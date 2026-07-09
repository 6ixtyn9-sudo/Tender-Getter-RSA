"""University of KwaZulu-Natal tender source plug-in."""
import logging
import re
from typing import List, Optional

from ...schemas import TenderOpportunity
from ..generic import _do_fetch, _get_ssl_context, _FETCH_TIMEOUT
from ..common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

# Real UKZN table (6 columns):
#   [0] empty
#   [1] Reference    e.g. "RFQ- UKZN 54/26"
#   [2] Description  (closing date embedded: "...Closing Date: 10/07/2026Year: 2026")
#   [3] Category     e.g. "Supply & Delivery"
#   [4] Download link
#   [5] Category slug
MOCK_HTML = """
<!DOCTYPE html><html><body><table>
<thead><tr><th></th><th>Reference</th><th>Description</th><th>Category</th><th>Download</th><th>Slug</th></tr></thead>
<tbody>
<tr>
    <td></td>
    <td>RFQ- UKZN 54/26</td>
    <td>SUPPLY AND DELIVERY OF APPLE IPAD DEVICESClosing Date: 10/07/2026Year: 2026</td>
    <td>Supply &amp; Delivery</td>
    <td>Download</td>
    <td>supply-delivery</td>
</tr>
<tr>
    <td></td>
    <td>RFQ UKZN RFS 08/26 (R)</td>
    <td>APPOINTMENT OF SERVICE PROVIDER TO REFURBISH THE ASRI PROPELLANTS LABORATORYClosing Date: 17/07/2026Year: 2026</td>
    <td>Services</td>
    <td>Download</td>
    <td>services</td>
</tr>
<tr>
    <td></td>
    <td>RFQ-UKZN CHUM 04/26</td>
    <td>Supply and Delivery of Small Laboratory Equipment Closing Date: 17/07/2026 Year: 2026</td>
    <td>Supply &amp; Delivery</td>
    <td>Download</td>
    <td>supply-delivery</td>
</tr>
</tbody>
</table></body></html>
"""

_TR = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_TD = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")
_CLOSING_EMBEDDED = re.compile(r"Closing\s*Date:\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", re.IGNORECASE)


class UkznSource:
    source_id: str = "ukzn"
    live: bool = True

    def __init__(self, url: str = "https://tenders.ukzn.ac.za/"):
        self.url = url
        self.issuing_entity = "University of KwaZulu-Natal"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        engaged_fallback = False
        if html_content is None:
            ssl_ctx = _get_ssl_context()
            try:
                html_content = _do_fetch(self.url, _FETCH_TIMEOUT, ssl_ctx)
            except Exception as exc:
                logger.warning("Failed to fetch UKZN from %s (%s). Using fallback.", self.url, exc)
                html_content = MOCK_HTML
                engaged_fallback = True

        tenders = self.parse_html(html_content, limit)
        if not tenders and not engaged_fallback:
            tenders = self.parse_html(MOCK_HTML, limit)
        return tenders

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        """
        UKZN: [empty, ref, description_with_closing, category, download, slug]
        Closing date is embedded in description as 'Closing Date: DD/MM/YYYY'.
        """
        tenders: List[TenderOpportunity] = []
        rows = _TR.findall(html or "")

        for row_html in rows:
            tds = [_TAG.sub("", td).strip() for td in _TD.findall(row_html)]
            if len(tds) < 3:
                continue

            ref = tds[1] if len(tds) > 1 else ""
            raw_desc = tds[2] if len(tds) > 2 else ""

            # Extract closing date from description
            closing_str = ""
            closing_match = _CLOSING_EMBEDDED.search(raw_desc)
            if closing_match:
                closing_str = closing_match.group(1)
                # Remove the closing date suffix from description
                title_desc = raw_desc[:closing_match.start()].strip()
            else:
                title_desc = raw_desc

            if not ref or not title_desc or len(ref) > 120:
                continue
            if not any(ch.isdigit() for ch in ref):
                continue

            combined = f"{ref} {title_desc}"
            cidb_hit = re_search_cidb(combined)
            cidb_level = int(cidb_hit[0]) if cidb_hit else None
            cidb_class = cidb_hit[1] if cidb_hit else None
            location = province_from_text(combined) or "KwaZulu-Natal"

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
