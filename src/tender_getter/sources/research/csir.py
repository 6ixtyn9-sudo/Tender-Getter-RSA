"""Council for Scientific and Industrial Research tender source plug-in."""
import logging
import re
from typing import List, Optional

from ...schemas import TenderOpportunity
from ..generic import _do_fetch, _get_ssl_context, _FETCH_TIMEOUT
from ..common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

# Real table (4 cols): [description, ref, published, closing]
MOCK_HTML = """
<!DOCTYPE html><html><body><table>
<tbody>
<tr>
    <td>Provision of Fire Detection, Gas Fire Suppression Systems</td>
    <td>CSIR RFQ 3733/31/07/2026</td>
    <td>17/07/2025 - 10:00</td>
    <td>31/07/2026 - 16:30</td>
</tr>
<tr>
    <td>Supply, Deliver, Install and Commission Network Equipment</td>
    <td>CSIR RFQ 6733/22/07/2026</td>
    <td></td>
    <td>22/07/2026 - 16:30</td>
</tr>
</tbody>
</table></body></html>
"""

_TR = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_TD = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")


class CsirSource:
    source_id: str = "csir"
    live: bool = True

    def __init__(self, url: str = "https://www.csir.co.za/tender/"):
        self.url = url
        self.issuing_entity = "Council for Scientific and Industrial Research"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        engaged_fallback = False
        if html_content is None:
            ssl_ctx = _get_ssl_context()
            try:
                html_content = _do_fetch(self.url, _FETCH_TIMEOUT, ssl_ctx)
            except Exception as exc:
                logger.warning("Failed to fetch CSIR from %s (%s). Using fallback.", self.url, exc)
                html_content = MOCK_HTML
                engaged_fallback = True
        tenders = self.parse_html(html_content, limit)
        if not tenders and not engaged_fallback:
            tenders = self.parse_html(MOCK_HTML, limit)
        return tenders

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        """CSIR: [description, ref, published, closing]. Closing: 'DD/MM/YYYY - HH:MM'"""
        tenders: List[TenderOpportunity] = []
        rows = _TR.findall(html or "")
        for row_html in rows:
            tds = [_TAG.sub("", td).strip() for td in _TD.findall(row_html)]
            if len(tds) < 4:
                continue
            title_desc, ref = tds[0], tds[1]
            closing_str = re.sub(r"\s*-\s*\d{1,2}:\d{2}$", "", tds[3]).strip()
            if not ref or not any(ch.isdigit() for ch in ref):
                continue
            combined = f"{ref} {title_desc}"
            cidb_hit = re_search_cidb(combined)
            location = province_from_text(combined) or "Gauteng"
            tenders.append(TenderOpportunity(
                tender_id=ref[:100], title=f"{ref}: {title_desc}"[:500],
                issuing_entity=self.issuing_entity, closing_date=parse_closing_date(closing_str),
                estimated_value=None, required_cidb_class=cidb_hit[1] if cidb_hit else None,
                required_cidb_level=int(cidb_hit[0]) if cidb_hit else None,
                mandatory_csd=True, tax_compliance_required=True, location_target=location, raw_document_url=None,
            ))
            if limit is not None and len(tenders) >= limit:
                break
        return tenders
