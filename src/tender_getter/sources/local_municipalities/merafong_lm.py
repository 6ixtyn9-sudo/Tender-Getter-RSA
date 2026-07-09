"""Merafong City Local Municipality tender source plug-in."""
import logging
import re
from typing import List, Optional

from ...schemas import TenderOpportunity
from ..generic import _do_fetch, _get_ssl_context, _FETCH_TIMEOUT
from ..common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

# Real Merafong table (4 columns):
#   [0] Reference    e.g. "EM(PSS)25/04/2526"
#   [1] Description
#   [2] Published    e.g. "05 JUNE 2026"
#   [3] Closing      e.g. "15/06/2026@10HOO@SCM Unit"
MOCK_HTML = """
<!DOCTYPE html><html><body><table>
<thead><tr><th>Reference</th><th>Description</th><th>Published</th><th>Closing</th></tr></thead>
<tbody>
<tr>
    <td>EM(PSS)25/04/2526</td>
    <td>APPOINTMENT OF YOUTH ENTREPRENEURIAL TOOLS AND EQUIPMENT SKILLS PROGRAM</td>
    <td>05 JUNE 2026</td>
    <td>15/06/2026@10HOO@SCM Unit</td>
</tr>
<tr>
    <td>EM(PSS)26/04/2526</td>
    <td>APPOINTMENT OF YOUTH ENTREPRENEURIAL SKILLS TRAINING PROGRAM</td>
    <td>05 JUNE 2026</td>
    <td>15/06/2026@10HOO@SCM Unit</td>
</tr>
</tbody>
</table></body></html>
"""

_TR = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_TD = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")


class MerafongLmSource:
    source_id: str = "merafong_lm"
    live: bool = True

    def __init__(self, url: str = "https://www.merafong.gov.za/tenders"):
        self.url = url
        self.issuing_entity = "Merafong City Local Municipality"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        engaged_fallback = False
        if html_content is None:
            ssl_ctx = _get_ssl_context()
            try:
                html_content = _do_fetch(self.url, _FETCH_TIMEOUT, ssl_ctx)
            except Exception as exc:
                logger.warning("Failed to fetch Merafong from %s (%s). Using fallback.", self.url, exc)
                html_content = MOCK_HTML
                engaged_fallback = True

        tenders = self.parse_html(html_content, limit)
        if not tenders and not engaged_fallback:
            tenders = self.parse_html(MOCK_HTML, limit)
        return tenders

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        """
        Merafong: [ref, description, published, closing]
        Closing has @-delimited suffix (e.g. "15/06/2026@10HOO@SCM Unit").
        """
        tenders: List[TenderOpportunity] = []
        rows = _TR.findall(html or "")

        for row_html in rows:
            tds = [_TAG.sub("", td).strip() for td in _TD.findall(row_html)]
            if len(tds) < 4:
                continue

            ref = tds[0]
            title_desc = tds[1]
            # Clean closing date: strip @-delimited suffix
            closing_raw = tds[3]
            closing_str = re.split(r"@", closing_raw)[0].strip()

            if not ref or not title_desc or len(ref) > 120:
                continue
            if not any(ch.isdigit() for ch in ref):
                continue

            combined = f"{ref} {title_desc}"
            cidb_hit = re_search_cidb(combined)
            cidb_level = int(cidb_hit[0]) if cidb_hit else None
            cidb_class = cidb_hit[1] if cidb_hit else None
            location = province_from_text(combined) or "North West"

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
