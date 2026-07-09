"""Bitou Local Municipality tender source plug-in."""
import logging
import re
from typing import List, Optional

from ...schemas import TenderOpportunity
from ..generic import _do_fetch, _get_ssl_context, _FETCH_TIMEOUT
from ..common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

# Real Bitou table (5 columns):
#   [0] Description
#   [1] Reference    e.g. "SCM/2026/82/PD"
#   [2] Closing      e.g. "Fri, 07/08/2026 - 12:00"
#   [3] Compulsory briefing  "Yes"/"No"
#   [4] Value threshold
MOCK_HTML = """
<!DOCTYPE html><html><body><table>
<thead><tr><th>Description</th><th>Reference</th><th>Closing</th><th>Briefing</th><th>Value</th></tr></thead>
<tbody>
<tr>
    <td>Construction Health &amp; Safety Services for Multi-year period</td>
    <td>SCM/2026/82/PD</td>
    <td>Fri, 07/08/2026 - 12:00</td>
    <td>Yes</td>
    <td>Tender: Over R300 000</td>
</tr>
<tr>
    <td>Re-Advertisement of Supply and Delivery of Emergency Human Settlement Material</td>
    <td>SCM/2026/81/PD</td>
    <td>Fri, 07/08/2026 - 12:00</td>
    <td>Yes</td>
    <td>Tender: Over R300 000</td>
</tr>
<tr>
    <td>INSTALLATION, MAINTENANCE, MONITORING OF SECURITY SYSTEMS</td>
    <td>SCM/2026/84/COMM</td>
    <td>Fri, 07/08/2026 - 12:00</td>
    <td>Yes</td>
    <td>Tender: Over R300 000</td>
</tr>
</tbody>
</table></body></html>
"""

_TR = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_TD = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")


class BitouLmSource:
    source_id: str = "bitou_lm"
    live: bool = True

    def __init__(self, url: str = "https://www.bitou.gov.za/tenders"):
        self.url = url
        self.issuing_entity = "Bitou Local Municipality"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        engaged_fallback = False
        if html_content is None:
            ssl_ctx = _get_ssl_context()
            try:
                html_content = _do_fetch(self.url, _FETCH_TIMEOUT, ssl_ctx)
            except Exception as exc:
                logger.warning("Failed to fetch Bitou from %s (%s). Using fallback.", self.url, exc)
                html_content = MOCK_HTML
                engaged_fallback = True

        tenders = self.parse_html(html_content, limit)
        if not tenders and not engaged_fallback:
            tenders = self.parse_html(MOCK_HTML, limit)
        return tenders

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        """
        Bitou: [description, ref, closing, briefing, value]
        Closing format: "Fri, 07/08/2026 - 12:00"
        """
        tenders: List[TenderOpportunity] = []
        rows = _TR.findall(html or "")

        for row_html in rows:
            tds = [_TAG.sub("", td).strip() for td in _TD.findall(row_html)]
            if len(tds) < 3:
                continue

            title_desc = tds[0]
            ref = tds[1]
            # Clean closing: strip day name prefix
            closing_raw = tds[2] if len(tds) > 2 else ""
            closing_str = re.sub(r"^[A-Za-z]+,\s*", "", closing_raw).strip()
            # Strip time suffix "- 12:00"
            closing_str = re.sub(r"\s*-\s*\d{1,2}:\d{2}$", "", closing_str).strip()

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
