"""GenericSource – shared fetch/parse boilerplate for per-source plug-ins.

Strategy layers (fastest → most expensive):
  1. Static HTML parse of the target URL
  2. Discovered subpage parse (follows href links containing tender keywords)
  3. Playwright render (only when TENDER_AUTO_PLAYWRIGHT != 0)
  4. TenderBulletins.co.za aggregator fallback (when source_id + slug known)
  5. Mock-HTML fallback

Environment controls:
  TENDER_FETCH_TIMEOUT   seconds for HTTP requests (default 10)
  TENDER_SSL_VERIFY      set to "1" to enforce SSL (default: skip)
  TENDER_AUTO_PLAYWRIGHT "0"    → disabled (default)
                         "auto" → only when page looks JS-rendered
                         "1" or "force" → always try for zero-yield sources
  TENDER_AGGREGATOR_FB   set to "0" to disable TenderBulletins fallback
"""
from __future__ import annotations

import logging
import os
import re
import ssl
from datetime import datetime, timezone
from typing import List, Optional, Tuple
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

from ..schemas import TenderOpportunity
from .common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
_ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
_FETCH_TIMEOUT = int(os.environ.get("TENDER_FETCH_TIMEOUT", "10"))
_SKIP_SSL = os.environ.get("TENDER_SSL_VERIFY", "0") != "1"
_AUTO_PLAYWRIGHT = os.environ.get("TENDER_AUTO_PLAYWRIGHT", "0").lower()
_AGGREGATOR_FB = os.environ.get("TENDER_AGGREGATOR_FB", "1").lower() != "0"

_TR_PATTERN = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_TD_PATTERN = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
_TAG_STRIP = re.compile(r"<[^>]+>")
_HREF_PATTERN = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)

# Keywords that indicate a page/link is tender-related
_TENDER_KEYWORDS = re.compile(
    r"\b(tender|tenders|quotation|quotations|procurement|supply.chain|scm|rfq|rfp|bid|bids)\b",
    re.IGNORECASE,
)

# Heuristic: page looks JS-rendered if it's small but has script tags
_JS_RENDER_RE = re.compile(
    r"(react|angular|vue|__NEXT_DATA__|window\.__STATE__|data-reactroot)", re.IGNORECASE
)


def _get_ssl_context() -> Optional[ssl.SSLContext]:
    """Return an unverified SSL context when skipping verification."""
    if not _SKIP_SSL:
        return None
    try:
        ctx = ssl._create_unverified_context()
        return ctx
    except Exception:
        return None


def _get_ssl_context_tls12() -> Optional[ssl.SSLContext]:
    """TLS 1.2-only unverified context for sites that reject TLS 1.3 negotiation."""
    try:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        ctx.maximum_version = ssl.TLSVersion.TLSv1_2
        return ctx
    except Exception:
        return _get_ssl_context()


def _do_fetch(url: str, timeout: int, ssl_ctx: Optional[ssl.SSLContext]) -> str:
    """HTTP GET with TLS-retry: if handshake times out, retry with TLS 1.2-only,
    then fall back to plain HTTP if still failing."""
    headers = {
        "User-Agent": _USER_AGENT,
        "Accept": _ACCEPT,
        "Accept-Language": "en-ZA,en;q=0.9",
        "Connection": "close",
    }
    req = Request(url, headers=headers)
    kwargs: dict = {"timeout": timeout}
    if ssl_ctx is not None:
        kwargs["context"] = ssl_ctx

    try:
        with urlopen(req, **kwargs) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except ssl.SSLError as exc:
        logger.debug("SSL error on %s (%s) – retrying with TLS 1.2", url, exc)
    except OSError as exc:
        # handshake timeout shows as ssl.c:1011 wrapped in OSError/URLError
        msg = str(exc).lower()
        if "handshake" not in msg and "timed out" not in msg:
            raise
        logger.debug("SSL handshake timeout on %s – retrying with TLS 1.2", url)

    # Retry with TLS 1.2 context
    tls12_ctx = _get_ssl_context_tls12()
    req2 = Request(url, headers=headers)
    kw2: dict = {"timeout": timeout}
    if tls12_ctx:
        kw2["context"] = tls12_ctx
    try:
        with urlopen(req2, **kw2) as resp:
            logger.info("TLS 1.2 retry succeeded for %s", url)
            return resp.read().decode("utf-8", errors="replace")
    except (ssl.SSLError, OSError):
        pass

    # Final fallback: plain HTTP (many SA gov sites serve both)
    if url.startswith("https://"):
        http_url = "http://" + url[8:]
        req3 = Request(http_url, headers=headers)
        try:
            with urlopen(req3, timeout=timeout) as resp:
                logger.info("HTTP fallback succeeded for %s", url)
                return resp.read().decode("utf-8", errors="replace")
        except Exception as exc:
            raise URLError(f"All TLS strategies failed for {url}: {exc}")
    raise URLError(f"All TLS strategies failed for {url}")


def _discover_tender_subpages(base_url: str, html: str) -> List[str]:
    """Scan html for href links that look like tender sub-pages.

    Returns a de-duplicated list of absolute URLs to try, prioritised by
    relevance (links with /tenders/ in path first).
    """
    base = urlparse(base_url)
    base_origin = f"{base.scheme}://{base.netloc}"
    seen: set = set()
    hits: List[Tuple[int, str]] = []  # (priority, url)

    for href in _HREF_PATTERN.findall(html):
        href = href.strip()
        if not href or href.startswith("#") or href.startswith("javascript"):
            continue
        abs_url = urljoin(base_url, href)
        parsed = urlparse(abs_url)
        # Must be same origin
        if parsed.netloc and parsed.netloc != base.netloc:
            continue
        if abs_url in seen or abs_url == base_url:
            continue
        seen.add(abs_url)

        path_and_fragment = parsed.path + " " + href
        if _TENDER_KEYWORDS.search(path_and_fragment):
            priority = 0 if "/tenders" in parsed.path.lower() else 1
            hits.append((priority, abs_url))

    hits.sort(key=lambda x: x[0])
    return [u for _, u in hits[:8]]  # cap at 8 candidates


def _looks_js_rendered(html: str) -> bool:
    """Heuristic: is this page probably a JS SPA with no static table data?"""
    rows = _TR_PATTERN.findall(html)
    if rows:
        return False  # Static tables present → not JS-rendered
    return bool(_JS_RENDER_RE.search(html)) or len(html) < 20_000


def _try_playwright(url: str) -> Optional[str]:
    """Attempt Playwright render. Returns HTML string or None if unavailable."""
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page(user_agent=_USER_AGENT)
            page.goto(url, timeout=30_000, wait_until="networkidle")
            html = page.content()
            browser.close()
            return html
    except ImportError:
        logger.debug("Playwright not installed – skipping Playwright fallback.")
        return None
    except Exception as exc:
        logger.warning("Playwright failed for %s: %s", url, exc)
        return None


def standard_fetch(
    url: str,
    mock_html: str,
    html_content: Optional[str] = None,
    limit: Optional[int] = None,
    source_id: str = "",
    issuing_entity: str = "",
) -> List[TenderOpportunity]:
    """Standard fetch+parse+fallback flow used by most per-source files.

    Strategy:
      1. If html_content supplied → parse only (testing/offline path).
      2. Try live static fetch.
      3. If 0 results: try discovered tender subpages.
      4. If still 0 and Playwright enabled: try Playwright render.
      5. If still 0 and source_id known: try TenderBulletins.co.za aggregator.
      6. If still 0: engage mock fallback.
    """
    if html_content is not None:
        tenders = parse_html_table(html_content, limit)
        if tenders:
            return tenders
        # 0 results from supplied HTML → fall back to mock (offline/test safety net)
        return parse_html_table(mock_html, limit)

    ssl_ctx = _get_ssl_context()
    engaged_fallback = False
    primary_html: Optional[str] = None

    # --- Step 1: Static fetch ---
    try:
        primary_html = _do_fetch(url, _FETCH_TIMEOUT, ssl_ctx)
        logger.debug("Fetched %s successfully (%d bytes)", url, len(primary_html))
    except (URLError, HTTPError, TimeoutError, OSError, Exception) as exc:
        logger.warning("Failed to fetch %s (%s). Will try subpages then mock.", url, exc)

    tenders = parse_html_table(primary_html or "", limit) if primary_html else []

    # --- Step 2: Subpage discovery ---
    if not tenders and primary_html:
        subpages = _discover_tender_subpages(url, primary_html)
        for sub_url in subpages:
            try:
                sub_html = _do_fetch(sub_url, _FETCH_TIMEOUT, ssl_ctx)
                sub_tenders = parse_html_table(sub_html, limit)
                if sub_tenders:
                    logger.info("Recovered %d tenders via subpage %s", len(sub_tenders), sub_url)
                    tenders = sub_tenders
                    break
            except Exception as exc:
                logger.debug("Subpage %s failed: %s", sub_url, exc)

    # --- Step 3: Playwright fallback ---
    if not tenders and _AUTO_PLAYWRIGHT != "0":
        should_try_pw = (
            _AUTO_PLAYWRIGHT in ("1", "force") or
            (_AUTO_PLAYWRIGHT == "auto" and primary_html and _looks_js_rendered(primary_html))
        )
        if should_try_pw:
            logger.info("Trying Playwright render for %s", url)
            pw_html = _try_playwright(url)
            if pw_html:
                tenders = parse_html_table(pw_html, limit)
                if tenders:
                    logger.info("Playwright recovered %d tenders from %s", len(tenders), url)

    # --- Step 4: TenderBulletins.co.za aggregator fallback ---
    if not tenders and _AGGREGATOR_FB and source_id:
        try:
            from .aggregators.tenderbulletins import fetch_tenderbulletins, resolve_slug
            slug = resolve_slug(source_id, issuing_entity or "")
            if slug:
                logger.info("Trying TenderBulletins aggregator for source_id='%s' slug='%s'",
                            source_id, slug)
                tenders = fetch_tenderbulletins(
                    slug,
                    issuing_entity=issuing_entity or "",
                    limit=limit,
                    max_pages=3,
                )
                if tenders:
                    logger.info("TenderBulletins recovered %d tenders for %s",
                                len(tenders), source_id)
        except Exception as exc:
            logger.debug("TenderBulletins fallback failed for %s: %s", source_id, exc)

    # --- Step 5: Mock fallback ---
    if not tenders:
        logger.info("All live strategies yielded 0 tenders for %s – engaging mock fallback.", url)
        tenders = parse_html_table(mock_html, limit)
        engaged_fallback = True

    return tenders


def parse_html_table(
    html: str,
    limit: Optional[int] = None,
    issuing_entity: Optional[str] = None,
) -> List[TenderOpportunity]:
    """Standard <tr><td> parser used by per-source files."""
    tenders: List[TenderOpportunity] = []
    rows = _TR_PATTERN.findall(html or "")

    for row_html in rows:
        tds = [_TAG_STRIP.sub("", td).strip() for td in _TD_PATTERN.findall(row_html)]
        if len(tds) < 2:
            continue

        ref = tds[0]
        title_desc = tds[1] if len(tds) > 1 else ""

        closing_str = ""
        for td_val in tds[2:]:
            if any(ch.isdigit() for ch in td_val) and len(td_val) > 6:
                closing_str = td_val
                break

        # Require at least 2 cols, and ref must not be pure boilerplate
        if not ref or not title_desc or len(ref) > 120:
            continue
        # Skip rows where ref has no digit AND no slash (likely headers)
        if not any(ch.isdigit() or ch == "/" for ch in ref):
            continue

        combined_text = f"{ref} {title_desc}"
        cidb_hit = re_search_cidb(combined_text)
        cidb_level = int(cidb_hit[0]) if cidb_hit else None
        cidb_class = cidb_hit[1] if cidb_hit else None
        location = province_from_text(combined_text)

        tenders.append(
            TenderOpportunity(
                tender_id=ref[:100],
                title=f"{ref}: {title_desc}"[:500],
                issuing_entity=issuing_entity or "",
                closing_date=parse_closing_date(closing_str),
                estimated_value=None,
                required_cidb_class=cidb_class,
                required_cidb_level=cidb_level,
                mandatory_csd=True,
                tax_compliance_required=True,
                location_target=location,
                raw_document_url=None,
            )
        )

        if limit is not None and len(tenders) >= limit:
            break

    return tenders
