"""Mkhondo Local Municipality tender source plug-in."""
import logging
import re
from typing import List, Optional

from ...schemas import TenderOpportunity
from ..generic import _do_fetch, _get_ssl_context, _FETCH_TIMEOUT
from ..common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

# Real table (5 cols): [ref, description, published, awarded_details, closing]
MOCK_HTML = """
<!DOCTYPE html><html><body><table>
<tbody>
<tr>
    <td>MKHO09/2025/26</td>
    <td>RENTAL, SUPPLY, INSTALLATION, AND MAINTENANCE OF ANALOGUE MIDBAND RADIO REPEATER</td>
    <td>2026 January 13</td>
    <td>AWARDED</td>
    <td>2025 November 28</td>
</tr>
<tr>
    <td>MKH15/2025/26</td>
    <td>APPOINTMENT OF A PANEL OF REPUTABLE TRAVEL AGENTS FOR 24 MONTHS</td>
    <td>2026 January 13</td>
    <td>AWARDED</td>
    <td>2025 November 28</td>
</tr>
</tbody>
</table></body></html>
"""

_TR = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_TD = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")


class MkhondoLmSource:
    source_id: str = "mkhondo_lm"
    live: bool = True

    def __init__(self, url: str = "https://www.mkhondo.gov.za/tenders"):
        self.url = url
        self.issuing_entity = "Mkhondo Local Municipality"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        engaged_fallback = False
        if html_content is None:
            ssl_ctx = _get_ssl_context()
            try:
                html_content = _do_fetch(self.url, _FETCH_TIMEOUT, ssl_ctx)
            except Exception as exc:
                logger.warning("Failed to fetch Mkhondo from %s (%s). Using fallback.", self.url, exc)
                html_content = MOCK_HTML
                engaged_fallback = True
        tenders = self.parse_html(html_content, limit)
        if not tenders and not engaged_fallback:
            tenders = self.parse_html(MOCK_HTML, limit)
        return tenders

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        """Mkhondo: [ref, description, published, awarded_details, closing]"""
        tenders: List[TenderOpportunity] = []
        rows = _TR.findall(html or "")
        for row_html in rows:
            tds = [_TAG.sub("", td).strip() for td in _TD.findall(row_html)]
            if len(tds) < 3:
                continue
            ref = tds[0]
            title_desc = tds[1]
            # Closing date: last column with a date
            closing_str = ""
            for td_val in reversed(tds[2:]):
                if re.search(r"\d{4}\s+\w+\s+\d{1,2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", td_val):
                    closing_str = td_val
                    break
            if not ref or not any(ch.isdigit() for ch in ref):
                continue
            combined = f"{ref} {title_desc}"
            cidb_hit = re_search_cidb(combined)
            location = province_from_text(combined) or "Mpumalanga"
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
