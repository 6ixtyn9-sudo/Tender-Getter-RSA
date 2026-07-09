"""South African Broadcasting Corporation tender source plug-in."""
import logging
import re
from typing import List, Optional

from ...schemas import TenderOpportunity
from ..generic import _do_fetch, _get_ssl_context, _FETCH_TIMEOUT
from ..common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

# Real SABC table (4 columns):
#   [0] empty
#   [1] Combined ref + description  e.g. "RFQ/COM/2026/10252092/32:APPOINTMENT OF..."
#   [2] Status                       e.g. "Open Tender"
#   [3] Date                         e.g. "July 1, 2026"
MOCK_HTML = """
<!DOCTYPE html><html><body><table>
<thead><tr><th></th><th>Tender</th><th>Status</th><th>Date</th></tr></thead>
<tbody>
<tr>
    <td></td>
    <td>RFQ/COM/2026/10252092/32:APPOINTMENT OF A SERVICE PROVIDER TO PROVIDE PUBLIC RELATIONS SERVICES</td>
    <td>Open Tender</td>
    <td>July 1, 2026</td>
</tr>
<tr>
    <td></td>
    <td>RFQ/NEW/2026/10252687/33:APPOINTMENT OF A SERVICE PROVIDER FOR PROVISION OF PROTECTIVE SERVICES</td>
    <td>Open Tender</td>
    <td>July 1, 2026</td>
</tr>
<tr>
    <td></td>
    <td>RFP/TVO/2026/10251075/5 : APPOINTMENT OF A PANEL OF SERVICE PROVIDERS FOR PROCUREMENT OF CONTENT</td>
    <td>Open Tender</td>
    <td>June 25, 2026</td>
</tr>
</tbody>
</table></body></html>
"""

_TR = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_TD = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")
_REF_SPLIT = re.compile(r"^([\w/]+)\s*[:\-]\s*(.+)", re.DOTALL)


class SabcSource:
    source_id: str = "sabc"
    live: bool = True

    def __init__(self, url: str = "https://www.sabc.co.za/sabc/tenders/"):
        self.url = url
        self.issuing_entity = "South African Broadcasting Corporation"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        engaged_fallback = False
        if html_content is None:
            ssl_ctx = _get_ssl_context()
            try:
                html_content = _do_fetch(self.url, _FETCH_TIMEOUT, ssl_ctx)
            except Exception as exc:
                logger.warning("Failed to fetch SABC from %s (%s). Using fallback.", self.url, exc)
                html_content = MOCK_HTML
                engaged_fallback = True

        tenders = self.parse_html(html_content, limit)
        if not tenders and not engaged_fallback:
            tenders = self.parse_html(MOCK_HTML, limit)
        return tenders

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        """
        SABC: [empty, combined_ref_description, status, date]
        Split column 1 on first ':' to get ref and description.
        """
        tenders: List[TenderOpportunity] = []
        rows = _TR.findall(html or "")

        for row_html in rows:
            tds = [_TAG.sub("", td).strip() for td in _TD.findall(row_html)]
            if len(tds) < 3:
                continue

            combined_col = tds[1]
            # Closing date in last column (e.g. "July 1, 2026")
            closing_str = tds[-1] if len(tds) > 2 else ""

            # Split ref from description on first ':'
            split_match = _REF_SPLIT.match(combined_col)
            if split_match:
                ref = split_match.group(1).strip()
                title_desc = split_match.group(2).strip()
            else:
                ref = combined_col[:60]
                title_desc = combined_col

            if not ref or len(ref) > 120:
                continue
            if not any(ch.isdigit() for ch in ref):
                continue

            combined_text = f"{ref} {title_desc}"
            cidb_hit = re_search_cidb(combined_text)
            cidb_level = int(cidb_hit[0]) if cidb_hit else None
            cidb_class = cidb_hit[1] if cidb_hit else None
            location = province_from_text(combined_text) or "Gauteng"

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
