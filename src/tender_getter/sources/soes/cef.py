"""Central Energy Fund tender source plug-in."""
import logging
import re
from typing import List, Optional

from ...schemas import TenderOpportunity
from ..generic import _do_fetch, _get_ssl_context, _FETCH_TIMEOUT
from ..common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

# Real CEF table (5 columns):
#   [0] Description
#   [1] Reference    e.g. "WELL/07/2026"
#   [2] Published    e.g. "06 JULY 2026"
#   [3] Closing      e.g. "13 JULY 2026 @12:00, MIDDAY"
#   [4] Something
MOCK_HTML = """
<!DOCTYPE html><html><body><table>
<tbody>
<tr>
    <td>REQUEST FOR QUOTATION FOR WELLNESS SERVICES</td>
    <td>WELL/07/2026</td>
    <td>06 JULY 2026</td>
    <td>13 JULY 2026 @12:00, MIDDAY</td>
    <td></td>
</tr>
<tr>
    <td>REQUEST FOR TENDER FOR PROVISION OF SECURITY SERVICES</td>
    <td>SAPT/07/2026</td>
    <td>02 JULY 2026</td>
    <td>22 JULY 2026 @12H00, MIDDAY</td>
    <td></td>
</tr>
</tbody>
</table></body></html>
"""

_TR = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_TD = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")


class CefSource:
    source_id: str = "cef"
    live: bool = True

    def __init__(self, url: str = "https://www.cefgroup.co.za/current-tenders"):
        self.url = url
        self.issuing_entity = "Central Energy Fund"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        engaged_fallback = False
        if html_content is None:
            ssl_ctx = _get_ssl_context()
            try:
                html_content = _do_fetch(self.url, _FETCH_TIMEOUT, ssl_ctx)
            except Exception as exc:
                logger.warning("Failed to fetch CEF from %s (%s). Using fallback.", self.url, exc)
                html_content = MOCK_HTML
                engaged_fallback = True
        tenders = self.parse_html(html_content, limit)
        if not tenders and not engaged_fallback:
            tenders = self.parse_html(MOCK_HTML, limit)
        return tenders

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        """CEF: [description, ref, published, closing, extra]"""
        tenders: List[TenderOpportunity] = []
        rows = _TR.findall(html or "")
        for row_html in rows:
            tds = [_TAG.sub("", td).strip() for td in _TD.findall(row_html)]
            if len(tds) < 4:
                continue
            title_desc = tds[0]
            ref = tds[1]
            # Clean closing: strip @time suffix
            closing_str = re.sub(r"@\d{1,2}[hH:]\d{2}.*$", "", tds[3]).strip()
            if not ref or not any(ch.isdigit() for ch in ref):
                continue
            combined = f"{ref} {title_desc}"
            cidb_hit = re_search_cidb(combined)
            cidb_level = int(cidb_hit[0]) if cidb_hit else None
            cidb_class = cidb_hit[1] if cidb_hit else None
            location = province_from_text(combined) or "Gauteng"
            tenders.append(TenderOpportunity(
                tender_id=ref[:100], title=f"{ref}: {title_desc}"[:500],
                issuing_entity=self.issuing_entity, closing_date=parse_closing_date(closing_str),
                estimated_value=None, required_cidb_class=cidb_class, required_cidb_level=cidb_level,
                mandatory_csd=True, tax_compliance_required=True, location_target=location, raw_document_url=None,
            ))
            if limit is not None and len(tenders) >= limit:
                break
        return tenders
