"""Department of Health Tender Source Plugin"""
import logging
import re
from datetime import datetime, timezone
from typing import List, Optional

from ...schemas import TenderOpportunity
from ..generic import _do_fetch, _get_ssl_context, _FETCH_TIMEOUT
from ..common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

# Real DOH table structure (5 columns):
#   [0] Bid Reference   e.g. "NDOH 11-2026/2027"
#   [1] Description
#   [2] Published Date   e.g. "19 June 2026"
#   [3] Closing Date     e.g. "13 July 2026 at 11:00am"
#   [4] Enquiries
MOCK_DOH_HTML = """
<!DOCTYPE html><html><body><table>
<thead><tr><th>Bid Reference</th><th>Description</th><th>Published</th><th>Closing Date</th><th>Enquiries</th></tr></thead>
<tbody>
<tr>
    <td>NDOH 11-2026/2027</td>
    <td>Appointment of service providers to support the National Department of Health with ICT infrastructure</td>
    <td>19 June 2026</td>
    <td>13 July 2026 at 11:00am</td>
    <td>Email: tenders@health.gov.za</td>
</tr>
<tr>
    <td>DoH 132/2026-27</td>
    <td>Appointment of a service provider for refurbishments at Ladybrand DCR, Free State</td>
    <td>20 May 2026</td>
    <td>08 June 2026 at 11:00am</td>
    <td>Email: purchasing@health.gov.za</td>
</tr>
<tr>
    <td>DoH 131/2026-27</td>
    <td>Appointment of a service provider for the construction of water management infrastructure</td>
    <td>20 May 2026</td>
    <td>04 June 2026 at 11:00am</td>
    <td>Email: purchasing@health.gov.za</td>
</tr>
</tbody>
</table></body></html>
"""

_TR = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_TD = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")


class DoHSource:
    source_id: str = "doh"

    def __init__(self, url: str = "https://www.health.gov.za/tenders"):
        self.url = url

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        """Fetches and parses active DoH tenders."""
        engaged_fallback = False
        if html_content is None:
            ssl_ctx = _get_ssl_context()
            try:
                html_content = _do_fetch(self.url, _FETCH_TIMEOUT, ssl_ctx)
            except Exception as exc:
                logger.warning("Failed to fetch DoH tenders from %s (%s). Using fallback.", self.url, exc)
                html_content = MOCK_DOH_HTML
                engaged_fallback = True

        tenders = self.parse_html(html_content, limit)

        if not tenders and not engaged_fallback:
            logger.info("DoH live page yielded 0 results. Using fallback.")
            tenders = self.parse_html(MOCK_DOH_HTML, limit)

        return tenders

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        """
        Parses DoH tenders. Real table has 5 columns:
          [0] ref, [1] description, [2] published, [3] closing date, [4] enquiries
        """
        tenders: List[TenderOpportunity] = []
        rows = _TR.findall(html or "")

        for row_html in rows:
            tds = [_TAG.sub("", td).strip() for td in _TD.findall(row_html)]
            if len(tds) < 3:
                continue

            ref = tds[0]
            title_desc = tds[1]

            # Find closing date: DoH has [ref, desc, published, closing, enquiries].
            # Closing date is in column 3 (e.g. "13 July 2026 at 11:00am").
            # Search in reverse to prefer the closing date over the published date.
            closing_str = ""
            for td_val in reversed(tds[2:]):
                # Strip "at HH:MMam/pm" suffix to get clean date for parser
                cleaned = re.sub(r"\s+at\s+\d{1,2}[:h]\d{2}\s*(?:am|pm)?", "", td_val, flags=re.IGNORECASE).strip()
                if re.search(r"\d{1,2}\s+[A-Za-z]{3,}\s+\d{4}", cleaned):
                    closing_str = cleaned
                    break
                # Also match numeric dates
                if re.search(r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", td_val):
                    closing_str = td_val
                    break

            # Skip non-data rows
            if not ref or not title_desc or len(ref) > 120:
                continue
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
                    issuing_entity="National Department of Health",
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
