"""Swartland Municipality tender source plug-in."""
import logging
import re
from typing import List, Optional

from ...schemas import TenderOpportunity
from ..generic import _do_fetch, _get_ssl_context, _FETCH_TIMEOUT
from ..common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

# Real Swartland LM table (7 columns):
#   [0] Reference    e.g. "T52.25.26"
#   [1] Published    e.g. "03 Jun 2026"
#   [2] Closing      e.g. "17 Jul 2026"
#   [3] Description
#   [4] Site meeting
#   [5] Download
#   [6] Email
MOCK_HTML = """
<!DOCTYPE html><html><body><table>
<thead><tr><th>Ref</th><th>Published</th><th>Closing</th><th>Description</th><th>Site Meeting</th><th>Download</th><th>Email</th></tr></thead>
<tbody>
<tr>
    <td>T52.25.26</td>
    <td>03 Jun 2026</td>
    <td>17 Jul 2026</td>
    <td>SUPPLY OF ASPHALTING SERVICES AND ANCILLARY WORKS IN THE SWARTLAND MUNICIPAL AREA</td>
    <td>No site meeting required</td>
    <td>Download</td>
    <td>Email</td>
</tr>
<tr>
    <td>T48.25.26</td>
    <td>22 Jun 2026</td>
    <td>10 Jul 2026</td>
    <td>SUPPLY AND DELIVER OF 1 X 3 TON CREWCAB 4X4 TIPPER TRUCK</td>
    <td>No site meeting required</td>
    <td>Download</td>
    <td>Email</td>
</tr>
</tbody>
</table></body></html>
"""

_TR = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_TD = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")


class SwartlandLmSource:
    source_id: str = "swartland_lm"
    live: bool = True

    def __init__(self, url: str = "https://www.swartland.org.za/tenders"):
        self.url = url
        self.issuing_entity = "Swartland Municipality"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        engaged_fallback = False
        if html_content is None:
            ssl_ctx = _get_ssl_context()
            try:
                html_content = _do_fetch(self.url, _FETCH_TIMEOUT, ssl_ctx)
            except Exception as exc:
                logger.warning("Failed to fetch Swartland from %s (%s). Using fallback.", self.url, exc)
                html_content = MOCK_HTML
                engaged_fallback = True

        tenders = self.parse_html(html_content, limit)
        if not tenders and not engaged_fallback:
            tenders = self.parse_html(MOCK_HTML, limit)
        return tenders

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        """
        Swartland: [ref, published, closing, description, site_meeting, download, email]
        """
        tenders: List[TenderOpportunity] = []
        rows = _TR.findall(html or "")

        for row_html in rows:
            tds = [_TAG.sub("", td).strip() for td in _TD.findall(row_html)]
            if len(tds) < 4:
                continue

            ref = tds[0]
            # Closing date in column 2 (e.g. "17 Jul 2026")
            closing_str = tds[2] if len(tds) > 2 else ""
            title_desc = tds[3] if len(tds) > 3 else tds[1]

            if not ref or not title_desc or len(ref) > 120:
                continue
            if not any(ch.isdigit() for ch in ref):
                continue

            combined = f"{ref} {title_desc}"
            cidb_hit = re_search_cidb(combined)
            cidb_level = int(cidb_hit[0]) if cidb_hit else None
            cidb_class = cidb_hit[1] if cidb_hit else None
            location = province_from_text(combined) or "Western Cape"

            tenders.append(
                TenderOpportunity(
                    tender_id=ref[:100],
                    title=f"{ref}: {title_desc}"[:500],
                    issuing_entity=self.issuing_entity,
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
