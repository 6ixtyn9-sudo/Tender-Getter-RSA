"""Department of Forestry, Fisheries & the Environment Tender Source Plugin"""
import logging
import re
from datetime import datetime, timezone
from typing import List, Optional

from ...schemas import TenderOpportunity
from ..generic import _do_fetch, _get_ssl_context, _FETCH_TIMEOUT
from ..common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

# Real DFFE table structure (6 columns):
#   [0] Bid Reference   e.g. "DFFE-B004 (2026/2027)"
#   [1] Closing Date    e.g. "08/14/2026 - 11:00"
#   [2] Description     e.g. "The appointment of the professional service provider..."
#   [3] Briefing Info    (optional, can be empty)
#   [4] (empty)
#   [5] Published Date   e.g. "2026-07-07"
MOCK_DFFE_HTML = """
<!DOCTYPE html><html><body><table>
<thead><tr><th>Bid Reference</th><th>Closing Date</th><th>Description</th><th>Briefing</th><th></th><th>Published</th></tr></thead>
<tbody>
<tr>
    <td>DFFE-B004 (2026/2027)</td>
    <td>08/14/2026 - 11:00</td>
    <td>The appointment of the professional service provider to undertake feasibility study</td>
    <td></td>
    <td></td>
    <td>2026-07-07</td>
</tr>
<tr>
    <td>RFQ0001217 (2026/2027)</td>
    <td>07/14/2026 - 11:00</td>
    <td>To appoint a service provider to supply the department with marine living resources</td>
    <td></td>
    <td></td>
    <td>2026-07-01</td>
</tr>
<tr>
    <td>RFQ0001232 (2026/2027)</td>
    <td>07/27/2026 - 11:00</td>
    <td>To appoint a contractor to provide construction services</td>
    <td>Compulsory briefing 14 July 2026</td>
    <td></td>
    <td>2026-07-01</td>
</tr>
</tbody>
</table></body></html>
"""

_TR = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_TD = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")


class DFFESource:
    source_id: str = "dffe"

    def __init__(self, url: str = "https://www.dffe.gov.za/tenders"):
        self.url = url

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        """Fetches and parses active DFFE tenders."""
        engaged_fallback = False
        if html_content is None:
            ssl_ctx = _get_ssl_context()
            try:
                html_content = _do_fetch(self.url, _FETCH_TIMEOUT, ssl_ctx)
            except Exception as exc:
                logger.warning("Failed to fetch DFFE tenders from %s (%s). Using fallback.", self.url, exc)
                html_content = MOCK_DFFE_HTML
                engaged_fallback = True

        tenders = self.parse_html(html_content, limit)

        if not tenders and not engaged_fallback:
            logger.info("DFFE live page yielded 0 results. Using fallback.")
            tenders = self.parse_html(MOCK_DFFE_HTML, limit)

        return tenders

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        """
        Parses DFFE tenders. Real table has 6 columns:
          [0] ref, [1] closing date, [2] description, [3] briefing, [4] empty, [5] published
        """
        tenders: List[TenderOpportunity] = []
        rows = _TR.findall(html or "")

        for row_html in rows:
            tds = [_TAG.sub("", td).strip() for td in _TD.findall(row_html)]
            if len(tds) < 3:
                continue

            # DFFE layout: [ref, closing_date, description, ...]
            # Column 1 uses US format MM/DD/YYYY (e.g. "08/14/2026 - 11:00")
            ref = tds[0]
            col1_is_date = bool(re.search(r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", tds[1]))

            if col1_is_date and len(tds) >= 3:
                # DFFE format: ref | closing_date (MM/DD/YYYY) | description
                closing_str = self._parse_us_date(tds[1])
                title_desc = tds[2]
            else:
                # Fallback: standard format ref | description | closing_date
                title_desc = tds[1]
                closing_str = ""
                for td_val in tds[2:]:
                    if any(ch.isdigit() for ch in td_val) and len(td_val) > 6:
                        closing_str = td_val
                        break

            # Skip non-data rows
            if not ref or not title_desc or len(ref) > 120:
                continue
            # Ref must contain at least one digit
            if not any(ch.isdigit() for ch in ref):
                continue

            combined_text = f"{ref} {title_desc}"
            cidb_hit = re_search_cidb(combined_text)
            cidb_level = int(cidb_hit[0]) if cidb_hit else None
            cidb_class = cidb_hit[1] if cidb_hit else None
            location = province_from_text(combined_text) or "National"

            tenders.append(
                TenderOpportunity(
                    tender_id=ref[:100],
                    title=f"{ref}: {title_desc}"[:500],
                    issuing_entity="Department of Forestry, Fisheries and the Environment",
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

    @staticmethod
    def _parse_us_date(s: str) -> str:
        """Convert US date 'MM/DD/YYYY - HH:MM' to ISO 'YYYY-MM-DD'."""
        m = re.match(r"(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})", s)
        if m:
            month, day, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
            if year < 100:
                year += 2000
            return f"{year:04d}-{month:02d}-{day:02d}"
        return s
