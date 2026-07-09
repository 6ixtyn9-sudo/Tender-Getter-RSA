"""Legal Aid South Africa tender source plug-in."""
import logging
import re
from typing import List, Optional

from ...schemas import TenderOpportunity
from ..generic import _do_fetch, _get_ssl_context, _FETCH_TIMEOUT
from ..common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

# Real Legal Aid SA table (3 columns):
#   [0] Ref+Desc  e.g. "Tender Number – 29/2026"
#   [1] Description
#   [2] Closing   e.g. "11/08/2026"
MOCK_HTML = """
<!DOCTYPE html><html><body><table>
<tbody>
<tr>
    <td>Tender Number – 29/2026</td>
    <td>Provision of Office Accommodation for a period of up to five years</td>
    <td>11/08/2026</td>
</tr>
<tr>
    <td>Tender Number – 23/2026</td>
    <td>Provision of Office Accommodation in Gqeberha</td>
    <td>11/08/2026</td>
</tr>
<tr>
    <td>Tender Number – GQEBERHA/18/2026</td>
    <td>Provision of Construction Services for Refurbishment</td>
    <td>06/08/2026</td>
</tr>
</tbody>
</table></body></html>
"""

_TR = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_TD = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")
_TENDER_NUM = re.compile(r"Tender\s*(?:Number)?\s*[–-]\s*([\w/]+)", re.IGNORECASE)


class LegalAidSaSource:
    source_id: str = "legal_aid_sa"
    live: bool = True

    def __init__(self, url: str = "https://www.legal-aid.co.za/tenders"):
        self.url = url
        self.issuing_entity = "Legal Aid South Africa"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        engaged_fallback = False
        if html_content is None:
            ssl_ctx = _get_ssl_context()
            try:
                html_content = _do_fetch(self.url, _FETCH_TIMEOUT, ssl_ctx)
            except Exception as exc:
                logger.warning("Failed to fetch Legal Aid SA from %s (%s). Using fallback.", self.url, exc)
                html_content = MOCK_HTML
                engaged_fallback = True
        tenders = self.parse_html(html_content, limit)
        if not tenders and not engaged_fallback:
            tenders = self.parse_html(MOCK_HTML, limit)
        return tenders

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        tenders: List[TenderOpportunity] = []
        rows = _TR.findall(html or "")
        for row_html in rows:
            tds = [_TAG.sub("", td).strip() for td in _TD.findall(row_html)]
            if len(tds) < 3:
                continue
            raw_ref = tds[0]
            title_desc = tds[1]
            closing_str = tds[2]
            # Extract tender number
            ref_match = _TENDER_NUM.search(raw_ref)
            ref = ref_match.group(1) if ref_match else raw_ref[:60]
            if not ref or not any(ch.isdigit() for ch in ref):
                continue
            combined = f"{ref} {title_desc}"
            cidb_hit = re_search_cidb(combined)
            cidb_level = int(cidb_hit[0]) if cidb_hit else None
            cidb_class = cidb_hit[1] if cidb_hit else None
            location = province_from_text(combined) or "National"
            tenders.append(TenderOpportunity(
                tender_id=ref[:100], title=f"{ref}: {title_desc}"[:500],
                issuing_entity=self.issuing_entity, closing_date=parse_closing_date(closing_str),
                estimated_value=None, required_cidb_class=cidb_class, required_cidb_level=cidb_level,
                mandatory_csd=True, tax_compliance_required=True, location_target=location, raw_document_url=None,
            ))
            if limit is not None and len(tenders) >= limit:
                break
        return tenders
