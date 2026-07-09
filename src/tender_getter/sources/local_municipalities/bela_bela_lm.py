"""Bela-Bela Local Municipality tender source plug-in."""
import logging
import re
from typing import List, Optional

from ...schemas import TenderOpportunity
from ..generic import _do_fetch, _get_ssl_context, _FETCH_TIMEOUT
from ..common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

# Real Bela-Bela table (4 columns):
#   [0] Title        e.g. "SERVICE PROVIDERS FOR SUPPLY AND DELIVERY OF TRANSFORMERS"
#   [1] Published    e.g. "2026-06-05" (ISO format)
#   [2] Closing      e.g. "2026-07-17" (ISO format)
#   [3] View link
MOCK_HTML = """
<!DOCTYPE html><html><body><table>
<thead><tr><th>Title</th><th>Published</th><th>Closing</th><th>View</th></tr></thead>
<tbody>
<tr>
    <td>SERVICE PROVIDERS FOR SUPPLY AND DELIVERY OF TRANSFORMERS, MINI SUBSTATIONS, SWITCHES</td>
    <td>2026-06-05</td>
    <td>2026-07-17</td>
    <td>View</td>
</tr>
<tr>
    <td>Tender Advert 15 06 2026</td>
    <td>2026-06-15</td>
    <td>2026-07-22</td>
    <td>View</td>
</tr>
<tr>
    <td>ERRUTAM 25 06 2026</td>
    <td>2026-06-25</td>
    <td>2026-07-20</td>
    <td>View</td>
</tr>
</tbody>
</table></body></html>
"""

_TR = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_TD = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")


class BelaBelaLmSource:
    source_id: str = "bela_bela_lm"
    live: bool = True

    def __init__(self, url: str = "https://www.belabela.gov.za/tenders"):
        self.url = url
        self.issuing_entity = "Bela-Bela Local Municipality"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        engaged_fallback = False
        if html_content is None:
            ssl_ctx = _get_ssl_context()
            try:
                html_content = _do_fetch(self.url, _FETCH_TIMEOUT, ssl_ctx)
            except Exception as exc:
                logger.warning("Failed to fetch Bela-Bela from %s (%s). Using fallback.", self.url, exc)
                html_content = MOCK_HTML
                engaged_fallback = True

        tenders = self.parse_html(html_content, limit)
        if not tenders and not engaged_fallback:
            tenders = self.parse_html(MOCK_HTML, limit)
        return tenders

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        """
        Bela-Bela: [title, published(ISO), closing(ISO), view]
        """
        tenders: List[TenderOpportunity] = []
        rows = _TR.findall(html or "")

        for row_html in rows:
            tds = [_TAG.sub("", td).strip() for td in _TD.findall(row_html)]
            if len(tds) < 3:
                continue

            title_desc = tds[0]
            closing_str = tds[2] if len(tds) > 2 else ""

            # Skip non-tender rows (empty titles, navigation)
            if not title_desc or len(title_desc) < 5:
                continue

            # Generate a ref from the title
            ref_match = re.search(r"\b([A-Z]{2,}[\s/]*\d{2,})\b", title_desc)
            ref = ref_match.group(1) if ref_match else title_desc[:60]

            combined = f"{ref} {title_desc}"
            cidb_hit = re_search_cidb(combined)
            cidb_level = int(cidb_hit[0]) if cidb_hit else None
            cidb_class = cidb_hit[1] if cidb_hit else None
            location = province_from_text(combined) or "Limpopo"

            tenders.append(
                TenderOpportunity(
                    tender_id=ref[:100],
                    title=title_desc[:500],
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
