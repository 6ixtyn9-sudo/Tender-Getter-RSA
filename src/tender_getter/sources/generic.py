"""GenericSource is a SMALL UTILITY used by per-source files to avoid
copy-pasting the same boilerplate. It is NOT used as a universal plug-in.

Every source in this codebase has its own file (sources/<dir>/<entity_id>.py)
and its own mock HTML fixture. GenericSource is only imported by those
per-source files when they want to inherit the standard <tr><td> parser.
Most per-source files just use the parser functions from common.py
directly without inheriting from GenericSource.

This file exists only so the per-source files can share the boilerplate
of (1) HTTP fetch with fallback, (2) <tr><td> parsing, (3) TenderOpportunity
construction. Adding a new source still means creating one Python file.
"""
from __future__ import annotations

import logging
import os
import re
import ssl
from datetime import datetime, timezone
from typing import List, Optional
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
# Default 10s; override with env TENDER_FETCH_TIMEOUT
_FETCH_TIMEOUT = int(os.environ.get("TENDER_FETCH_TIMEOUT", "10"))
# SSL verification: set TENDER_SSL_VERIFY=1 to enforce (default: skip for gov sites)
_SKIP_SSL = os.environ.get("TENDER_SSL_VERIFY", "0") != "1"

_TR_PATTERN = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_TD_PATTERN = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
_TAG_STRIP = re.compile(r"<[^>]+>")


def _get_ssl_context() -> Optional[ssl.SSLContext]:
    """Return an unverified SSL context when skipping verification."""
    if not _SKIP_SSL:
        return None
    try:
        return ssl._create_unverified_context()
    except Exception:
        return None


def _do_fetch(url: str, timeout: int, ssl_ctx: Optional[ssl.SSLContext]) -> str:
    """Single HTTP GET; raises on failure."""
    req = Request(url, headers={"User-Agent": _USER_AGENT, "Accept": _ACCEPT})
    kwargs: dict = {"timeout": timeout}
    if ssl_ctx is not None:
        kwargs["context"] = ssl_ctx
    with urlopen(req, **kwargs) as resp:
        return resp.read().decode("utf-8", errors="replace")


def standard_fetch(url: str, mock_html: str, html_content: Optional[str] = None, limit: Optional[int] = None) -> List[TenderOpportunity]:
    """Standard fetch+parse+fallback flow used by most per-source files.

    Strategy:
      1. If html_content supplied, parse only (testing / offline path).
      2. Try live fetch with unverified SSL (most SA gov sites have broken certs).
      3. On failure, engage mock fallback.

    Returns the parsed list of TenderOpportunity instances.
    """
    engaged_fallback = False
    if html_content is None:
        ssl_ctx = _get_ssl_context()
        try:
            html_content = _do_fetch(url, _FETCH_TIMEOUT, ssl_ctx)
            logger.debug("Fetched %s successfully", url)
        except (URLError, HTTPError, TimeoutError, OSError, Exception) as exc:
            logger.warning("Failed to fetch %s (%s). Engaging mock fallback.", url, exc)
            html_content = mock_html
            engaged_fallback = True

    tenders = parse_html_table(html_content, limit)

    if not tenders and not engaged_fallback:
        logger.info("Live page %s parsed to 0 tenders - engaging mock fallback.", url)
        tenders = parse_html_table(mock_html, limit)

    return tenders


def parse_html_table(html: str, limit: Optional[int] = None, issuing_entity: Optional[str] = None) -> List[TenderOpportunity]:
    """Standard <tr><td> parser used by per-source files."""
    tenders: List[TenderOpportunity] = []
    rows = _TR_PATTERN.findall(html or "")

    for row_html in rows:
        tds = [_TAG_STRIP.sub("", td).strip() for td in _TD_PATTERN.findall(row_html)]
        if len(tds) < 3:
            continue

        ref = tds[0]
        title_desc = tds[1]

        closing_str = ""
        for td_val in tds[2:]:
            if any(ch.isdigit() for ch in td_val) and len(td_val) > 6:
                closing_str = td_val
                break

        if not ref or not title_desc or len(ref) > 100 or not any(ch.isdigit() for ch in ref):
            continue

        combined_text = f"{ref} {title_desc}"
        cidb_hit = re_search_cidb(combined_text)
        cidb_level = int(cidb_hit[0]) if cidb_hit else None
        cidb_class = cidb_hit[1] if cidb_hit else None
        location = province_from_text(combined_text)

        tenders.append(
            TenderOpportunity(
                tender_id=ref,
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
