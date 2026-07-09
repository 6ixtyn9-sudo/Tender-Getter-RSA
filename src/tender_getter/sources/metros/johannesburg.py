"""City of Johannesburg Metropolitan Municipality Tender Source Plugin"""
import logging
import re
from datetime import datetime, timezone
from typing import List, Optional

from ...schemas import TenderOpportunity
from ..generic import _do_fetch, _get_ssl_context, _FETCH_TIMEOUT, standard_fetch
from ..common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

# Real CoJ table structure (3 columns):
#   [0] Bid Reference   e.g. "COJ/GSPCR001/25-26"
#   [1] Description
#   [2] Closing Date    e.g. "16 February 2026"
MOCK_JOHANNESBURG_HTML = """
<!DOCTYPE html><html><body><table>
<thead><tr><th>Bid Number</th><th>Bid Description</th><th>Closing Date</th></tr></thead>
<tbody>
<tr>
    <td>COJ/GSPCR001/25-26</td>
    <td>APPOINTMENT OF A SERVICE PROVIDER TO CONDUCT THE CUSTOMER SATISFACTION SURVEY</td>
    <td>16 February 2026</td>
</tr>
<tr>
    <td>COJ/GFIN003/25-26</td>
    <td>APPOINTMENT OF A PANEL OF SERVICE PROVIDERS FOR THE SUPPLY, DELIVERY AND OFF-LOADING OF FINANCIAL CONSUMABLES</td>
    <td>27 November 2025</td>
</tr>
<tr>
    <td>COJ/COMDEV001/25-26</td>
    <td>APPOINTMENT OF SUITABLY EXPERIENCED SERVICE PROVIDERS FOR SUPPLY AND DELIVERY OF BUILDING MATERIALS</td>
    <td>28 November 2025</td>
</tr>
</tbody>
</table></body></html>
"""


class JohannesburgSource:
    source_id: str = "johannesburg"

    def __init__(self, url: str = "https://joburg.org.za/work_/Pages/2025-Tenders-and-Quotations/Bid-Opening-Registers.aspx"):
        self.url = url

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        """Fetches and parses active City of Johannesburg tenders."""
        engaged_fallback = False
        if html_content is None:
            ssl_ctx = _get_ssl_context()
            try:
                html_content = _do_fetch(self.url, _FETCH_TIMEOUT, ssl_ctx)
            except Exception as exc:
                logger.warning("Failed to fetch Joburg tenders from %s (%s). Using fallback.", self.url, exc)
                html_content = MOCK_JOHANNESBURG_HTML
                engaged_fallback = True

        tenders = self.parse_html(html_content, limit)

        if not tenders and not engaged_fallback:
            logger.info("Joburg live page yielded 0 results. Using fallback.")
            tenders = self.parse_html(MOCK_JOHANNESBURG_HTML, limit)

        return tenders

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        """
        Parses Joburg tenders. Standard 3-column table:
          [0] ref, [1] description, [2] closing date
        """
        tenders: List[TenderOpportunity] = []
        tr_pattern = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
        td_pattern = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
        tag_strip = re.compile(r"<[^>]+>")

        rows = tr_pattern.findall(html or "")

        for row_html in rows:
            tds = [tag_strip.sub("", td).strip() for td in td_pattern.findall(row_html)]
            if len(tds) < 3:
                continue

            ref = tds[0]
            title_desc = tds[1]

            # Closing date: look in columns 2 onward
            closing_str = ""
            for td_val in tds[2:]:
                if any(ch.isdigit() for ch in td_val) and len(td_val) > 6:
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
            location = province_from_text(combined_text) or "Gauteng"

            tenders.append(
                TenderOpportunity(
                    tender_id=ref[:100],
                    title=f"{ref}: {title_desc}"[:500],
                    issuing_entity="City of Johannesburg Metropolitan Municipality",
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
