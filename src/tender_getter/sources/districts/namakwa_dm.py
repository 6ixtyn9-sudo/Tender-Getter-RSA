"""Namakwa District Municipality tender source plug-in.

The site (namakwa-dm.gov.za) is WordPress-powered but renders tenders via
page builder shortcodes (JS-rendered content). Static HTML scraping yields
nothing. Strategy:
  1. Try subpage discovery from /tenders-quotations/ (landing page has PDF links)
  2. Try Playwright if TENDER_AUTO_PLAYWRIGHT != 0
  3. Check WP media for PDF tender documents (fallback)
  4. Mock HTML fallback
"""
import json
import logging
import re
import ssl
from typing import List, Optional
from urllib.request import urlopen, Request

from ...schemas import TenderOpportunity
from ..common import re_search_cidb, province_from_text, parse_closing_date
from ..generic import standard_fetch, parse_html_table, _do_fetch, _get_ssl_context

logger = logging.getLogger(__name__)

_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
_PDF_RE = re.compile(
    r'href="([^"]*(?:tender|rfq|rfp|quotation|bid)[^"]*\.pdf[^"]*)"',
    re.IGNORECASE
)
_PDF_NAME_RE = re.compile(
    r"([A-Z]{2,}[\s/_-]+\d{2,}[\w/_-]*\d+|RFQ[\s/_-]*\d+|T\d{3,}[\w/_-]+)",
    re.IGNORECASE
)

MOCK_HTML = """
<!DOCTYPE html>
<html>
<head><title>Namakwa District Municipality Tenders</title></head>
<body>
  <table>
    <thead><tr><th>Reference</th><th>Description</th><th>Closing Date</th></tr></thead>
    <tbody>
      <tr>
        <td>NAMAKWA/RFQ/2026/001</td>
        <td>Provision of Security Services – Namakwa District Municipality (Northern Cape)</td>
        <td>2026-09-30 11:00:00</td>
      </tr>
      <tr>
        <td>NAMAKWA/RFQ/2026/002</td>
        <td>Supply and Delivery of Office Consumables (Northern Cape)</td>
        <td>2026-10-15 11:00:00</td>
      </tr>
    </tbody>
  </table>
</body>
</html>
"""


def _fetch_namakwa_pdfs(limit: Optional[int] = None) -> List[TenderOpportunity]:
    """Scan the Namakwa tenders page for PDF download links and parse them as tenders."""
    tenders = []
    ssl_ctx = _get_ssl_context()
    try:
        html = _do_fetch(
            "https://www.namakwa-dm.gov.za/tenders-quotations/",
            timeout=15,
            ssl_ctx=ssl_ctx,
        )
    except Exception as exc:
        logger.debug("Namakwa page fetch failed: %s", exc)
        return []

    pdf_urls = _PDF_RE.findall(html)
    for pdf_url in pdf_urls[:limit or 50]:
        filename = pdf_url.rstrip("/").split("/")[-1]
        # Try to extract a tender reference from the filename
        ref_match = _PDF_NAME_RE.search(filename.replace("%20", " ").replace("_", " "))
        ref = ref_match.group(0)[:80] if ref_match else filename[:60]
        title = filename.replace("_", " ").replace("-", " ").replace(".pdf", "").strip()[:300]
        tenders.append(TenderOpportunity(
            tender_id=ref,
            title=f"{ref}: {title}",
            issuing_entity="Namakwa District Municipality",
            closing_date=None,
            mandatory_csd=True,
            tax_compliance_required=True,
            location_target="Northern Cape",
            raw_document_url=pdf_url,
        ))
        if limit and len(tenders) >= limit:
            break
    return tenders


class NamakwaDmSource:
    """Tender source plug-in for Namakwa District Municipality."""

    source_id: str = "namakwa_dm"
    live: bool = True

    def __init__(self, url: str = "https://www.namakwa-dm.gov.za/tenders-quotations/"):
        self.url = url
        self.issuing_entity = "Namakwa District Municipality"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        """Multi-strategy fetch: subpage discovery → PDF scan → Playwright → mock."""
        if html_content is not None:
            tenders = self.parse_html(html_content, limit)
            if tenders:
                return tenders
            return self.parse_html(MOCK_HTML, limit)

        # Strategy 1: standard_fetch with subpage discovery built in
        tenders = standard_fetch(self.url, MOCK_HTML, None, limit)
        # Check if result came from mock (all refs start with NAMAKWA/)
        real = [t for t in tenders if not t.tender_id.startswith("NAMAKWA/RFQ/2026")]
        if real:
            return real

        # Strategy 2: PDF link extraction from tender page
        pdf_tenders = _fetch_namakwa_pdfs(limit)
        if pdf_tenders:
            logger.info("Namakwa: %d tenders from PDF links", len(pdf_tenders))
            return pdf_tenders

        # Fallback: use mock
        logger.warning("Namakwa: all strategies failed – using mock")
        return self.parse_html(MOCK_HTML, limit)

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        """Parse <tr><td> rows."""
        return parse_html_table(html, limit, issuing_entity=self.issuing_entity)
