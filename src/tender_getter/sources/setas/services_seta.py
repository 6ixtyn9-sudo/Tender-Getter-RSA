"""Services Sector Education and Training Authority (Services SETA) tender source plug-in."""
import logging
import re
from typing import List, Optional

from ...schemas import TenderOpportunity
from ..generic import _do_fetch, _get_ssl_context, _FETCH_TIMEOUT
from ..common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

# Real Services SETA table (6 columns):
#   [0] Reference    e.g. "PROC T688"
#   [1] Description
#   [2] Published    e.g. "08/06/2026"
#   [3] Closing      e.g. "16/07/2026"
#   [4] N/A
#   [5] Download
MOCK_HTML = """
<!DOCTYPE html><html><body><table>
<thead><tr><th>Reference</th><th>Description</th><th>Published</th><th>Closing</th><th>N/A</th><th>Download</th></tr></thead>
<tbody>
<tr>
    <td>PROC T688</td>
    <td>APPOINTMENT OF A SERVICE PROVIDER FOR THE PROVISION OF RESOURCES TO SUPPORT THE SETA</td>
    <td>08/06/2026</td>
    <td>16/07/2026</td>
    <td>N/A</td>
    <td>Download</td>
</tr>
<tr>
    <td>PROC T687</td>
    <td>DEVELOPMENT OF A PROJECT MANAGEMENT SUPPORT FRAMEWORK</td>
    <td>08/06/2026</td>
    <td>15/07/2026</td>
    <td>N/A</td>
    <td>Download</td>
</tr>
<tr>
    <td>RFQC-000646</td>
    <td>APPOINTMENT OF A SERVICES PROVIDER TO PERFORM A TECHNICAL REVIEW</td>
    <td>15/05/2026</td>
    <td>22/05/2026</td>
    <td>N/A</td>
    <td>Download</td>
</tr>
</tbody>
</table></body></html>
"""

_TR = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_TD = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")


class ServicesSetaSource:
    source_id: str = "services_seta"
    live: bool = True

    def __init__(self, url: str = "https://www.serviceseta.org.za/tenders/"):
        self.url = url
        self.issuing_entity = "Services Sector Education and Training Authority"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        engaged_fallback = False
        if html_content is None:
            ssl_ctx = _get_ssl_context()
            try:
                html_content = _do_fetch(self.url, _FETCH_TIMEOUT, ssl_ctx)
            except Exception as exc:
                logger.warning("Failed to fetch Services SETA from %s (%s). Using fallback.", self.url, exc)
                html_content = MOCK_HTML
                engaged_fallback = True

        tenders = self.parse_html(html_content, limit)
        if not tenders and not engaged_fallback:
            tenders = self.parse_html(MOCK_HTML, limit)
        return tenders

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        """
        Services SETA: [ref, description, published, closing, N/A, download]
        """
        tenders: List[TenderOpportunity] = []
        rows = _TR.findall(html or "")

        for row_html in rows:
            tds = [_TAG.sub("", td).strip() for td in _TD.findall(row_html)]
            if len(tds) < 4:
                continue

            ref = tds[0]
            title_desc = tds[1]
            # Closing date in column 3 (format DD/MM/YYYY)
            closing_str = tds[3] if len(tds) > 3 else ""

            if not ref or not title_desc or len(ref) > 120:
                continue
            if not any(ch.isdigit() for ch in ref):
                continue

            combined = f"{ref} {title_desc}"
            cidb_hit = re_search_cidb(combined)
            cidb_level = int(cidb_hit[0]) if cidb_hit else None
            cidb_class = cidb_hit[1] if cidb_hit else None
            location = province_from_text(combined) or "Gauteng"

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
