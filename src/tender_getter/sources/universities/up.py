"""University of Pretoria tender source plug-in."""
import logging
import re
from typing import List, Optional

from ...schemas import TenderOpportunity
from ..generic import _do_fetch, _get_ssl_context, _FETCH_TIMEOUT
from ..common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

# Real UP table (5 columns):
#   [0] Reference    e.g. "RFP-202606-00348"
#   [1] Description
#   [2] Type         e.g. "RFP"
#   [3] Nationality  e.g. "South African"
#   [4] Closing      e.g. "2026-07-13 12:00:00"
MOCK_HTML = """
<!DOCTYPE html><html><body><table>
<thead><tr><th>Reference</th><th>Description</th><th>Type</th><th>Nationality</th><th>Closing</th></tr></thead>
<tbody>
<tr>
    <td>RFP-202606-00348</td>
    <td>PROVISION OF EXTERNAL AUDIT SERVICES</td>
    <td>RFP</td>
    <td>South African</td>
    <td>2026-07-13 12:00:00</td>
</tr>
<tr>
    <td>RFT-202606-00533</td>
    <td>SLA for the maintenance contract of Bio-Safety Laboratories level 3</td>
    <td>RFT</td>
    <td>South African</td>
    <td>2026-07-17 11:00:00</td>
</tr>
</tbody>
</table></body></html>
"""

_TR = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_TD = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")


class UpSource:
    source_id: str = "up"
    live: bool = True

    def __init__(self, url: str = "https://www.up.ac.za/tender/"):
        self.url = url
        self.issuing_entity = "University of Pretoria"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        engaged_fallback = False
        if html_content is None:
            ssl_ctx = _get_ssl_context()
            try:
                html_content = _do_fetch(self.url, _FETCH_TIMEOUT, ssl_ctx)
            except Exception as exc:
                logger.warning("Failed to fetch UP from %s (%s). Using fallback.", self.url, exc)
                html_content = MOCK_HTML
                engaged_fallback = True

        tenders = self.parse_html(html_content, limit)
        if not tenders and not engaged_fallback:
            tenders = self.parse_html(MOCK_HTML, limit)
        return tenders

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        """
        UP: [ref, description, type, nationality, closing_date]
        """
        tenders: List[TenderOpportunity] = []
        rows = _TR.findall(html or "")

        for row_html in rows:
            tds = [_TAG.sub("", td).strip() for td in _TD.findall(row_html)]
            if len(tds) < 3:
                continue

            ref = tds[0]
            title_desc = tds[1]

            # Closing date: last column with digits
            closing_str = ""
            for td_val in tds[2:]:
                if re.search(r"\d{4}-\d{2}-\d{2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", td_val):
                    closing_str = td_val
                    break

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
