"""tender_enrichment.py — open tender documents and extract full structured info.

THE PROBLEM THIS SOLVES:
  Surface scraping gives thin data (0.6% of tenders had CIDB, 0% had value).
  The real fields live INSIDE the tender PDFs. This module opens those documents
  and extracts: CIDB class/level, estimated value, closing date, bid number,
  B-BBEE points system, location — then writes them back onto the tender.

PIPELINE (per tender):
  1. resolve a document URL (raw_document_url, or discover via doc_finder)
  2. download the PDF (cached on disk)
  3. extract text with pdfplumber
     - TEXT-rich PDF  -> local regex extraction (fast, free, no API key)
     - SCANNED PDF    -> Gemini 1.5 vision OCR (requires GEMINI_API_KEY)
  4. merge extracted fields onto the TenderOpportunity and persist to DB

Gemini is used only when needed and only when a key is present, so the chain is
fully runnable now (text PDFs) and upgrades automatically (scanned PDFs) once
GEMINI_API_KEY is added to .env.

SECURE VERSION: SSL verification with certifi, proper error handling.
"""
from __future__ import annotations

import io
import json
import logging
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

from ..schemas import TenderOpportunity

logger = logging.getLogger(__name__)

DOC_CACHE_DIR = Path(__file__).resolve().parents[2] / "localdata" / "tender_docs"
_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

# A PDF is "text-rich" if pdfplumber finds this many chars in the screened pages.
_TEXT_THRESHOLD = 200


# ---------------------------------------------------------------------------
# Local regex field extractor (tuned for SA government tender language)
# ---------------------------------------------------------------------------

_CIDB_CLASS_RE = re.compile(
    r"\bCIDB[^.\n]{0,60}?grading[^.\n]{0,40}?(?:(\d)\s*([A-Z]{2}))\b"
    r"|\bgrading\s+designation[^.\n]{0,30}?(?:(\d)\s*([A-Z]{2}))\b"
    r"|\b(?:(?:minimum\s+)?CIDB\s*(?:grading|grade|class)[^.\n]{0,30}?)?(?<!\w)(\d)(GB|CE|ME|EE|EB|EP|SB|SO|SI|SL|SJ|SK|SF|SG|SH|SM|SN|SQ|SC|SD|SE|SP)(?!\w)",
    re.IGNORECASE,
)
_VALID_CIDB = {"GB", "CE", "ME", "EE", "EB", "EP", "SB", "SO", "SI", "SL", "SJ",
               "SK", "SF", "SG", "SH", "SM", "SN", "SQ", "SC", "SD", "SE", "SP"}

# Value: "R 5 600 000", "R5,6 million", "estimated value of R3 000 000.00"
_VALUE_RE = re.compile(
    r"(?:estimated\s+(?:contract\s+)?value|tender\s+value|contract\s+value|value\s*[:\\-]|"
    r"not\s+exceeding|NTE|in\s+excess\s+of)[^R]{0,15}R\s?([\d][\d ,\.]{3,})"
    r"|R\s?([\d]{1,3}(?:[ ,]\d{3})+)[^.]{0,20}(?:excl|vat|million|value)",
    re.IGNORECASE,
)
_MILLION_RE = re.compile(r"R\s?([\d.,]+)\s*(?:million|mil)\b", re.IGNORECASE)

_CLOSING_RE = re.compile(
    r"(?:closing\s+(?:date|time)|closes?\s+on|submit[^.\n]{0,20}by|deadline)[^:\n]{0,15}"
    r"[:\\-]?\s*((?:\d{1,2}[\s/-]+\w+[\s/-]+\d{2,4})|(?:\w+\s+\d{1,2},?\s+\d{4})|(?:\d{4}/\d{1,2}/\d{1,2})|(?:\d{1,2}\s+\w+\s+\d{4}))",
    re.IGNORECASE,
)

_BID_NO_RE = re.compile(
    r"(?:tender|bid|RFQ|RFP|RFT)\s*(?:no\.?|number|#|ref(?:erence)?)\s*[:\\-]?\s*([A-Z0-9][A-Z0-9/\-_\.]{3,24})",
    re.IGNORECASE,
)

_BBBEE_SYS_RE = re.compile(r"\b(80\s*/\s*20|90\s*/\s*10)\b")
_PROVINCE_HINT_RE = re.compile(
    r"\b(Gauteng|Western\s+Cape|Eastern\s+Cape|KwaZulu.Natal|Limpopo|Mpumalanga|"
    r"North\s+West|Northern\s+Cape|Free\s+State)\b", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Gemini API key pool — rotate across multiple keys to dodge free-tier 429s
# ---------------------------------------------------------------------------

class GeminiKeyPool:
    """Round-robin pool of Gemini API keys with per-key cooldown on rate-limit.

    Loads keys from env in either format:
      GEMINI_API_KEY=key1,key2,key3        (comma-separated)
      GEMINI_API_KEY_1=k1 GEMINI_API_KEY_2=k2 ... (numbered, up to _9)
    Both can be combined. Keys are deduped.
    """

    _COOLDOWN_S = 60  # how long to park a key after a 429

    def __init__(self):
        self._keys: list[str] = []
        self._idx = 0
        self._cooldown: dict[int, float] = {}
        self._load()

    def _load(self):
        import time
        raw = os.environ.get("GEMINI_API_KEY", "")
        if "," in raw:
            self._keys += [k.strip() for k in raw.split(",") if k.strip()]
        elif raw.strip():
            self._keys.append(raw.strip())
        for i in range(1, 10):
            k = os.environ.get(f"GEMINI_API_KEY_{i}", "").strip()
            if k:
                self._keys.append(k)
        self._keys = list(dict.fromkeys(self._keys))  # dedupe, preserve order

    def get(self) -> Optional[str]:
        """Return the next available key, or None if all are on cooldown."""
        import time
        now = time.time()
        n = len(self._keys)
        for _ in range(n):
            if self._cooldown.get(self._idx, 0) <= now:
                return self._keys[self._idx]
            self._idx = (self._idx + 1) % n
        return None

    def advance(self):
        """Move to the next key (after a successful call, for load-balancing)."""
        if self._keys:
            self._idx = (self._idx + 1) % len(self._keys)

    def mark_rate_limited(self, cooldown_s: Optional[float] = None):
        """Park the current key and rotate to the next."""
        import time
        self._cooldown[self._idx] = time.time() + (cooldown_s or self._COOLDOWN_S)
        self.advance()

    @property
    def total(self) -> int:
        return len(self._keys)

    @property
    def available(self) -> int:
        import time
        now = time.time()
        return sum(1 for i in range(len(self._keys)) if self._cooldown.get(i, 0) <= now)

    def __repr__(self):
        return f"GeminiKeyPool({self.total} keys, {self.available} available)"


_KEY_POOL: Optional["GeminiKeyPool"] = None


def _key_pool() -> "GeminiKeyPool":
    global _KEY_POOL
    if _KEY_POOL is None:
        _KEY_POOL = GeminiKeyPool()
    return _KEY_POOL


# ---------------------------------------------------------------------------
# Gemini structured output (forces valid JSON at the API level)
# ---------------------------------------------------------------------------

_GEMINI_SCHEMA = {
    "type": "object",
    "properties": {
        "required_cidb_class": {
            "type": "string",
            "enum": ["GB", "CE", "ME", "EE", "EB", "EP", "SB", "SO", "SI", "SL",
                     "SJ", "SK", "SF", "SG", "SH", "SM", "SN", "SQ", "SC", "SD",
                     "SE", "SP"],
        },
        "required_cidb_level": {"type": "integer", "minimum": 1, "maximum": 9},
        "estimated_value": {"type": "number"},
        "closing_date": {"type": "string"},
        "bid_number": {"type": "string"},
        "bbbee_points_system": {"type": "string", "enum": ["80/20", "90/10"]},
        "location_target": {"type": "string"},
    },
}

GEMINI_MODEL = os.environ.get("GEMINI_MODEL_VISION", "gemini-flash-latest")

_GEMINI_PROMPT = (
    "You are an expert South African government procurement document parser. "
    "The attached document is a tender/bid advert or SBD form. Read it carefully "
    "(it may be a scanned image — use OCR). Extract these fields:\n"
    "- required_cidb_class: the CIDB grading class required (e.g. CE, GB, EE, ME)\n"
    "- required_cidb_level: the CIDB grade level 1-9\n"
    "- estimated_value: the estimated/tender contract value in ZAR (number only)\n"
    "- closing_date: the closing/submission date as YYYY-MM-DD\n"
    "- bid_number: the official bid/tender reference number\n"
    "- bbbee_points_system: '80/20' or '90/10' if the PPPFA preference system is stated\n"
    "- location_target: the province name if work is localised, else 'National'\n"
    "Return null for any field not found in the document.\n"
)

def _trim_pdf(pdf_bytes: bytes, max_pages: int = 8) -> bytes:
    """Extract the first max_pages to cut token cost for Gemini.

    SBD forms and compliance details are almost always in the first few pages.
    Falls back to the full PDF on any error.
    """
    try:
        from pypdf import PdfReader, PdfWriter
        reader = PdfReader(io.BytesIO(pdf_bytes))
        if len(reader.pages) <= max_pages:
            return pdf_bytes
        writer = PdfWriter()
        for page in reader.pages[:max_pages]:
            writer.add_page(page)
        buf = io.BytesIO()
        writer.write(buf)
        return buf.getvalue()
    except Exception:
        return pdf_bytes


def extract_fields_local(text: str) -> dict:
    """Run regex extractors over PDF text. Returns only fields found."""
    from ..sources.common import parse_closing_date, province_from_text
    out: dict = {}

    # CIDB
    for m in _CIDB_CLASS_RE.finditer(text or ""):
        groups = m.groups()
        # the pattern has alternation; find the filled pair
        for i in range(0, len(groups), 2):
            lvl, cls = groups[i], groups[i + 1]
            if lvl and cls:
                cls = cls.upper()
                if cls in _VALID_CIDB:
                    out["required_cidb_class"] = cls
                    out["required_cidb_level"] = int(lvl)
                    break
        if "required_cidb_class" in out:
            break

    # Value
    if _VALUE_RE.search(text or ""):
        digits = _VALUE_RE.search(text).group(1) or _VALUE_RE.search(text).group(2)
        val = float(re.sub(r"[^\d]", "", digits))
        if val > 0:
            out["estimated_value"] = val
    elif _MILLION_RE.search(text or ""):
        val = float(_MILLION_RE.search(text).group(1).replace(",", "")) * 1_000_000
        if val > 0:
            out["estimated_value"] = val

    # Closing date
    cm = _CLOSING_RE.search(text or "")
    if cm:
        from ..sources.common import parse_closing_date
        cd = parse_closing_date(cm.group(1))
        if cd.year < 2099:
            out["closing_date"] = cd

    # Bid number
    bm = _BID_NO_RE.search(text or "")
    if bm:
        out["bid_number"] = bm.group(1).strip()

    # B-BBEE system
    bsm = _BBBEE_SYS_RE.search(text or "")
    if bsm:
        out["bbbee_points_system"] = bsm.group(1).replace(" ", "")

    # Province hint
    pm = _PROVINCE_HINT_RE.search(text or "")
    if pm:
        from ..sources.common import province_from_text
        prov = province_from_text(pm.group(0))
        if prov:
            out["location_target"] = prov

    return out


# ---------------------------------------------------------------------------
# Gemini vision extraction (for scanned PDFs) — key pool + structured output
# ---------------------------------------------------------------------------

def _extract_fields_gemini(pdf_bytes: bytes, mime: str = "application/pdf") -> dict:
    """Send the PDF to Gemini vision via REST with key rotation + structured JSON.

    Trims to first ~8 pages (SBD forms live up front), sends with responseSchema
    so Gemini MUST return valid JSON. Rotates across all available keys on 429.
    """
    import base64

    pool = _key_pool()
    if pool.total == 0:
        raise RuntimeError("No GEMINI_API_KEY set")

    trimmed = _trim_pdf(pdf_bytes)
    max_bytes = 18_000_000
    b64 = base64.b64encode(trimmed[:max_bytes]).decode()

    payload = json.dumps({
        "contents": [{"parts": [
            {"text": _GEMINI_PROMPT},
            {"inline_data": {"mime_type": mime, "data": b64}},
        ]}],
        "generationConfig": {
            "temperature": 0,
            "maxOutputTokens": 8192,  # thinking models need headroom to reason + answer
            "responseMimeType": "application/json",
            "responseSchema": _GEMINI_SCHEMA,
        },
    }).encode()

    kw_base = {"timeout": 90}
    ctx = ssl.create_default_context(cafile=certifi.where())
    ctx.check_hostname = True
    ctx.verify_mode = ssl.CERT_REQUIRED
    kw_base["context"] = ctx

    last_err = None
    for _attempt in range(pool.total):
        api_key = pool.get()
        if api_key is None:
            raise _GeminiRateBlocked(
                f"All {pool.total} keys on cooldown (rate-limited)")

        url = (f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}"
               f":generateContent?key={api_key}")
        req = Request(url, data=payload, headers={"Content-Type": "application/json"})
        try:
            with urlopen(req, context=ctx, timeout=90) as resp:
                data = json.loads(resp.read())
            pool.advance()  # spread load round-robin
            break
        except HTTPError as exc:
            if exc.code == 429:
                logger.info("Key %d/%d rate-limited — rotating.",
                            pool._idx + 1, pool.total)
                pool.mark_rate_limited()
                last_err = exc
                continue
            raise RuntimeError(
                f"Gemini API error {exc.code}: {exc.read().decode()[:200]}") from exc
    else:
        raise _GeminiRateBlocked(f"All keys exhausted. Last error: {last_err}")

    raw = (data.get("candidates", [{}])[0]
           .get("content", {})
           .get("parts", [{}])[0]
           .get("text", ""))
    result = _parse_gemini_json(raw)
    if result is None:
        logger.warning("Gemini returned unparseable JSON: %s", raw[:200])
        return {}

    # Clean sentinel values (model sometimes returns N/A / -1 instead of null)
    for k, v in list(result.items()):
        if v in (None, "N/A", "n/a", "NA", "", "null"):
            result[k] = None
        elif k in ("estimated_value", "required_cidb_level") and isinstance(v, (int, float)) and v <= 0:
            result[k] = None

    if result.get("closing_date"):
        from ..sources.common import parse_closing_date
        cd = parse_closing_date(result["closing_date"])
        if cd.year < 2099:
            result["closing_date"] = cd
        else:
            result.pop("closing_date", None)
    return result


class _GeminiRateBlocked(Exception):
    """All keys are rate-limited; caller should stop calling Gemini."""
    pass


# ---------------------------------------------------------------------------
# Download + per-tender enrichment (SECURE: SSL verification)
# ---------------------------------------------------------------------------

def _parse_gemini_json(raw: str) -> Optional[dict]:
    """Parse Gemini's JSON output robustly — handles code fences, single quotes,
    trailing commas, and partial JSON."""
    if not raw:
        return None
    clean = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
    # Try direct parse
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        pass
    # Try to extract just the {...} block
    m = re.search(r"\{.*\}", clean, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass
    # Last resort: fix common issues (single quotes, trailing commas)
    fixed = clean.replace("'", '"').rstrip(",")
    try:
        return json.loads(fixed)
    except json.JSONDecodeError:
        return None


def download_pdf(url: str, cache_key: Optional[str] = None) -> Optional[bytes]:
    """Download a PDF, cached by cache_key under localdata/tender_docs/.
    
    SECURE: SSL verification with certifi, proper timeout.
    """
    DOC_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if cache_key:
        safe = re.sub(r"[^A-Za-z0-9]+", "_", cache_key)[:80]
        cached = DOC_CACHE_DIR / f"{safe}.pdf"
        if cached.exists() and cached.stat().st_size > 0:
            return cached.read_bytes()
    req = Request(url, headers={"User-Agent": _UA, "Accept": "application/pdf,*/*"})
    kw = {"timeout": 25}
    ctx = ssl.create_default_context(cafile=certifi.where())
    ctx.check_hostname = True
    ctx.verify_mode = ssl.CERT_REQUIRED
    kw["context"] = ctx
    try:
        with urlopen(req, **kw) as r:
            data = r.read()
    except (URLError, HTTPError, OSError, TimeoutError) as exc:
        logger.warning("download failed %s: %s", url, exc)
        return None
    if cache_key and data[:4] == b"%PDF":
        safe = re.sub(r"[^A-Za-z0-9]+", "_", cache_key)[:80]
        (DOC_CACHE_DIR / f"{safe}.pdf").write_bytes(data)
    return data if data[:4] == b"%PDF" else None


def enrich_tender(
    tender: TenderOpportunity,
    doc_url: Optional[str] = None,
    use_gemini: bool = True,
) -> tuple[dict, str]:
    """Open a tender's document and extract fields.

    Returns (extracted_fields_dict, method) where method is one of:
    'local_regex', 'gemini_vision', 'no_doc', 'failed'.
    """
    url = doc_url or tender.raw_document_url
    if not url:
        return {}, "no_doc"

    pdf_bytes = download_pdf(url, cache_key=tender.tender_id)
    if not pdf_bytes:
        return {}, "failed"

    # Extract text
    text = ""
    n_pages = 0
    try:
        import pdfplumber  # type: ignore
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            n_pages = len(pdf.pages)
            for p in pdf.pages[:10]:
                text += (p.extract_text() or "") + "\n"
    except Exception as exc:
        logger.warning("pdfplumber failed for %s: %s", tender.tender_id, exc)

    if len(text) >= _TEXT_THRESHOLD:
        return extract_fields_local(text), "local_regex"

    # Scanned PDF -> Gemini vision
    if use_gemini and os.environ.get("GEMINI_API_KEY"):
        try:
            return _extract_fields_gemini(pdf_bytes), "gemini_vision"
        except HTTPError as exc:
            if exc.code == 429:
                logger.info("Gemini rate-limited (429). Stopping enrichment for this batch.")
                raise _GeminiRateBlocked()
            logger.warning("Gemini HTTP %s for %s", exc.code, tender.tender_id)
            return {}, "failed"
        except _GeminiRateBlocked:
            raise
        except Exception as exc:
            logger.warning("Gemini vision failed for %s: %s", tender.tender_id, exc)
            return {}, "failed"

    logger.info("Scanned PDF for %s but no GEMINI_API_KEY set — skipped.", tender.tender_id)
    return {}, "failed"


def apply_fields(tender: TenderOpportunity, fields: dict) -> TenderOpportunity:
    """Return a copy of the tender with extracted fields merged (non-destructive:
    only fills fields that are currently empty)."""
    if fields.get("required_cidb_class") and not tender.required_cidb_class:
        tender.required_cidb_class = fields["required_cidb_class"]
        if fields.get("required_cidb_level"):
            tender.required_cidb_level = fields["required_cidb_level"]
    if fields.get("estimated_value") and not tender.estimated_value:
        tender.estimated_value = fields["estimated_value"]
    if fields.get("closing_date") and tender.closing_date.year >= 2099:
        tender.closing_date = fields["closing_date"]
    if fields.get("location_target") and not tender.location_target:
        tender.location_target = fields["location_target"]
    return tender


class _GeminiRateBlocked(Exception):
    """All keys are rate-limited; caller should stop calling Gemini."""
    pass