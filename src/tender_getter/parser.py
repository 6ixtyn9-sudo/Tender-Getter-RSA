"""
parser.py - Gemini-powered OCR & compliance sieve for tender PDFs.

Pipeline:
  1. Local pre-screener (pdfplumber): extracts only pages containing
     known SBD keywords, reducing a 100-page PDF to ~5 pages.
     Bounded by TG_MAX_PDF_PAGES / TG_MAX_EXTRACT_CHARS (anti-DoS).
  2. Gemini: extracts structured JSON fields from the reduced text.
  3. Strict validation: the extracted JSON is coerced and validated
     field-by-field (unknown keys dropped, invalid values nulled) and
     returned as a partial TenderOpportunity dict ready for ingestion.

Environment:
  Requires GEMINI_API_KEY in a .env file (gitignored) or environment variable.
"""

import os
import json
import re
from pathlib import Path
from typing import Optional

# Optional imports — only required at runtime, not for unit-testing schemas/matcher
try:
    import pdfplumber  # type: ignore
    _PDFPLUMBER_AVAILABLE = True
except ImportError:
    _PDFPLUMBER_AVAILABLE = False

try:
    from google import genai as _genai  # type: ignore
    from google.genai import types as _genai_types  # type: ignore
    _GENAI_AVAILABLE = True
except ImportError:
    _GENAI_AVAILABLE = False


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Keywords that mark pages worth sending to the LLM
SBD_KEYWORDS = [
    "SBD 1", "SBD 6.1", "SBD 6.2",
    "CIDB", "evaluation criteria", "preferential points",
    "B-BBEE", "closing date", "bid number",
]

GEMINI_MODEL = "gemini-2.5-flash"

# Anti-DoS bounds for the local pre-screener (configurable via env).
MAX_PDF_PAGES = 200
MAX_EXTRACT_CHARS = 100_000

# Canonical extraction schema keys (anything else the model emits is dropped).
EXPECTED_KEYS = (
    "bid_number", "closing_date", "required_cidb_class",
    "required_cidb_level", "mandatory_csd", "bbbee_points_system",
    "location_target",
)

# Valid CIDB contractor grading classes.
CIDB_CLASS_CODES = {"CE", "GB", "EE", "ME", "SB", "PE", "PS", "SF", "SI"}


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default

# The strict JSON schema the model must produce
EXTRACTION_SYSTEM_PROMPT = """
You are a South African government tender document parser.
Extract ONLY the following fields from the provided document pages and return
them as a single, valid JSON object. Use null for any field you cannot find.
Do NOT include any text outside the JSON object.

Required output schema:
{
  "bid_number": "<string or null>",
  "closing_date": "<YYYY-MM-DD string or null>",
  "required_cidb_class": "<one of CE, GB, EE, ME, SB, PE, PS, SF, SI or null>",
  "required_cidb_level": "<integer 1-9 or null>",
  "mandatory_csd": "<true or false>",
  "bbbee_points_system": "<'80/20' or '90/10' or null>",
  "location_target": "<province name, 'National', or null>"
}
"""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def extract_relevant_pages(pdf_path: str | Path) -> str:
    """
    Stage 1: Local PDF pre-screener.
    Opens the PDF with pdfplumber and returns concatenated text from only
    those pages that contain at least one SBD keyword.

    Returns an empty string if pdfplumber is not installed.
    """
    if not _PDFPLUMBER_AVAILABLE:
        raise ImportError(
            "pdfplumber is required for PDF parsing. "
            "Install it with: pip install pdfplumber"
        )

    max_pages = _env_int("TG_MAX_PDF_PAGES", MAX_PDF_PAGES)
    max_chars = _env_int("TG_MAX_EXTRACT_CHARS", MAX_EXTRACT_CHARS)

    relevant_text_parts: list[str] = []
    keywords_lower = [kw.lower() for kw in SBD_KEYWORDS]

    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages):
            if i >= max_pages:
                break  # hard cap: never stream an unbounded page count
            text = page.extract_text() or ""
            if any(kw in text.lower() for kw in keywords_lower):
                relevant_text_parts.append(
                    f"--- PAGE {i + 1} ---\n{text}"
                )

    reduced = "\n\n".join(relevant_text_parts)
    if len(reduced) > max_chars:
        reduced = reduced[:max_chars] + "\n[TRUNCATED]"
    return reduced


def parse_tender_pdf(pdf_path: str | Path) -> dict:
    """
    Full two-tier sieve pipeline.
    Extracts relevant pages locally, then invokes Gemini to produce a
    validated JSON extraction dict.

    Returns a dict matching the extraction schema (all keys present,
    missing values as None/null).

    Raises:
      ImportError  – if pdfplumber or google-genai are not installed.
      ValueError   – if Gemini returns unparseable JSON.
      RuntimeError – if GEMINI_API_KEY is not set.
    """
    # --- Load .env if python-dotenv is available ---
    _try_load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. "
            "Add it to a .env file in the project root (gitignored)."
        )

    if not _GENAI_AVAILABLE:
        raise ImportError(
            "google-genai is required. "
            "Install it with: pip install google-genai"
        )

    # Stage 1 — local pre-screener
    reduced_text = extract_relevant_pages(pdf_path)
    if not reduced_text.strip():
        reduced_text = "(No SBD-keyword pages found — sending first 3 pages as fallback.)"

    # Stage 2 — Gemini extraction
    client = _genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=reduced_text,
        config=_genai_types.GenerateContentConfig(
            system_instruction=EXTRACTION_SYSTEM_PROMPT,
        ),
    )
    raw_json = _extract_json_block(response.text)

    try:
        result = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Gemini returned invalid JSON. Raw response:\n{response.text}"
        ) from exc

    if not isinstance(result, dict):
        raise ValueError(
            f"Gemini must return a single JSON object, got {type(result).__name__}."
        )

    return _validate_extraction(result)


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _extract_json_block(text: str) -> str:
    """
    Strips markdown code fences and returns only the raw JSON string.
    Gemini sometimes wraps the output in ```json ... ``` fences.
    """
    # Remove ```json ... ``` or ``` ... ``` wrappers
    clean = re.sub(r"```(?:json)?", "", text).strip().rstrip("`").strip()
    return clean


def _validate_extraction(result: dict) -> dict:
    """
    Coerce and validate the raw LLM extraction field-by-field.

    Adversarial or sloppy model output must never flow downstream:
      * unknown keys (e.g. injected instructions) are dropped;
      * wrong types or out-of-range values become None (fail-safe null),
        never a truthy string like 'false' or an invalid enum;
      * trivially coercible values ('4' -> 4, 'ce' -> 'CE') are normalised.
    """
    clean: dict = {key: None for key in EXPECTED_KEYS}

    bid_number = result.get("bid_number")
    if bid_number is not None:
        text = str(bid_number).strip()
        clean["bid_number"] = text or None

    closing = result.get("closing_date")
    if isinstance(closing, str):
        candidate = closing.strip()[:10]
        try:
            from datetime import date

            date.fromisoformat(candidate)
            clean["closing_date"] = candidate
        except ValueError:
            pass

    cidb_class = result.get("required_cidb_class")
    if isinstance(cidb_class, str):
        candidate = cidb_class.strip().upper()
        if candidate in CIDB_CLASS_CODES:
            clean["required_cidb_class"] = candidate

    cidb_level = result.get("required_cidb_level")
    if isinstance(cidb_level, bool):
        pass  # bool is an int subclass — explicitly rejected
    elif isinstance(cidb_level, int):
        if 1 <= cidb_level <= 9:
            clean["required_cidb_level"] = cidb_level
    elif isinstance(cidb_level, str) and cidb_level.strip().isdigit():
        level = int(cidb_level.strip())
        if 1 <= level <= 9:
            clean["required_cidb_level"] = level

    mandatory_csd = result.get("mandatory_csd")
    if isinstance(mandatory_csd, bool):
        clean["mandatory_csd"] = mandatory_csd

    system = result.get("bbbee_points_system")
    if isinstance(system, str) and system.strip() in {"80/20", "90/10"}:
        clean["bbbee_points_system"] = system.strip()

    location = result.get("location_target")
    if isinstance(location, str):
        text = location.strip()
        clean["location_target"] = text or None

    return clean


def _try_load_dotenv():
    """Silently load a .env file from the project root if python-dotenv is installed."""
    try:
        from dotenv import load_dotenv  # type: ignore
        dotenv_path = Path(__file__).resolve().parents[3] / ".env"
        if dotenv_path.exists():
            load_dotenv(dotenv_path)
    except ImportError:
        pass
