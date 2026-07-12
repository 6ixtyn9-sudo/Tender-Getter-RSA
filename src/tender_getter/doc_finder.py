"""doc_finder.py — recover tender document (PDF) URLs from live source pages.

WHY THIS EXISTS:
  The standard table parser strips all HTML tags, so every <a href> pointing at
  a tender PDF is thrown away (0/3839 tenders carry a raw_document_url). To
  actually OPEN and PARSE tender documents, we first need their URLs.

STRATEGY (does NOT touch generic.py — safe for the 725 dependent sources):
  Given a source URL, fetch its HTML and extract candidate document links:
    1. Direct PDF/document links (href ending in .pdf, .doc(x), or matching
       tender keywords) inside <td> cells or anywhere on the page.
    2. Detail-page links (a tender list row linking to a per-tender page that
       itself hosts the PDF).
  Match each document URL back to a tender_id by proximity in the table row.

This is a read-only discovery layer; it returns {tender_id: doc_url} mappings.
"""
from __future__ import annotations

import logging
import re
from typing import Optional
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser

from .sources.generic import _do_fetch, _get_ssl_context, _FETCH_TIMEOUT

logger = logging.getLogger(__name__)

_DOC_EXTS = re.compile(r"\.(?:pdf|docx?|xlsx?)(?:\?|#|$)", re.IGNORECASE)
_TENDER_HREF_RE = re.compile(
    r"(tender|bid|quotation|rfq|rfp|procurement|sbd|advert|notice)", re.IGNORECASE
)


class _LinkTableParser(HTMLParser):
    """Walks an HTML table and yields (cell_text, href) pairs per row, plus
    standalone (text, href) links. Robust to messy gov-site HTML."""

    def __init__(self):
        super().__init__()
        self.rows: list[list[dict]] = []  # each row = list of {text, href}
        self.links: list[tuple[str, str]] = []  # (text, href) anywhere
        self._cur_row: Optional[list[dict]] = None
        self._cur_cell: Optional[dict] = None
        self._cur_cell_hrefs: list[str] = []  # all hrefs in current cell
        self._cur_href: Optional[str] = None
        self._cur_text: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "tr":
            self._cur_row = []
        elif tag in ("td", "th"):
            self._cur_cell = {"text": "", "href": None}
            self._cur_cell_hrefs = []
        elif tag == "a" and "href" in a:
            self._cur_href = a["href"]

    def handle_data(self, data):
        text = data.strip()
        if text:
            self._cur_text.append(text)
            if self._cur_href is not None:
                self.links.append((text, self._cur_href))

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._cur_cell is not None:
            self._cur_cell["text"] = " ".join(self._cur_text)
            self._cur_text = []
            # Pick the first doc-looking href from this cell's links
            if self._cur_cell_hrefs:
                self._cur_cell["href"] = self._cur_cell_hrefs[0]
            if self._cur_row is not None:
                self._cur_row.append(self._cur_cell)
            self._cur_cell = None
            self._cur_cell_hrefs = []
            self._cur_href = None
        elif tag == "tr" and self._cur_row is not None:
            if self._cur_row:
                self.rows.append(self._cur_row)
            self._cur_row = None
        elif tag == "a":
            # Save href to the current cell BEFORE clearing (</a> fires before </td>)
            if self._cur_href is not None and self._cur_cell is not None:
                self._cur_cell_hrefs.append(self._cur_href)
            self._cur_href = None


def _is_doc_url(href: str, base_netloc: str) -> bool:
    if not href:
        return False
    if href.startswith(("javascript", "#", "mailto")):
        return False
    if _DOC_EXTS.search(href):
        return True
    parsed = urlparse(href)
    if parsed.netloc and parsed.netloc != base_netloc:
        return False
    return bool(_TENDER_HREF_RE.search(parsed.path)) and "wp-json" not in href


def find_document_urls(
    page_url: str,
    timeout: Optional[int] = None,
) -> dict[str, str]:
    """Fetch a tender page and return {tender_ref: doc_url} for every row that
    has a document link. tender_ref is derived from the row's first cell text."""
    timeout = timeout or _FETCH_TIMEOUT
    base_netloc = urlparse(page_url).netloc
    try:
        html = _do_fetch(page_url, timeout, _get_ssl_context())
    except Exception as exc:
        logger.warning("doc_finder: could not fetch %s: %s", page_url, exc)
        return {}

    parser = _LinkTableParser()
    try:
        parser.feed(html)
    except Exception:
        pass

    mappings: dict[str, str] = {}

    # 1) Table rows: pair a row's ref text with that row's document href
    for row in parser.rows:
        ref = ""
        doc_href = None
        for cell in row:
            t = cell.get("text", "")
            if not ref and t:
                ref = t  # first non-empty cell = ref
            if cell.get("href") and _is_doc_url(cell["href"], base_netloc):
                doc_href = cell["href"]
        if doc_href and ref:
            mappings[ref[:100]] = urljoin(page_url, doc_href)

    # 2) Standalone links (non-table pages): use link text as ref
    if not mappings:
        for text, href in parser.links:
            if _is_doc_url(href, base_netloc) and len(text) > 3:
                mappings[text[:100]] = urljoin(page_url, href)

    return mappings


def find_document_url_for_tender(
    page_url: str,
    tender_ref: str,
) -> Optional[str]:
    """Convenience: find the doc URL for a specific tender reference."""
    if not tender_ref:
        return None
    mappings = find_document_urls(page_url)
    if tender_ref in mappings:
        return mappings[tender_ref]
    # fuzzy: ref appears as substring of a key or vice-versa
    ref_l = tender_ref.lower()
    for key, url in mappings.items():
        if ref_l in key.lower() or key.lower() in ref_l:
            return url
    return None
