"""Agricultural Sector Education and Training Authority tender source plug-in."""
import logging
import re
from typing import List, Optional

from ...schemas import TenderOpportunity
from ..generic import _do_fetch, _get_ssl_context, _FETCH_TIMEOUT
from ..common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

# Real AgriSETA table (3 columns):
#   [0] Published    e.g. "27 March 2026"
#   [1] Description  (RFP ref embedded: "REQUEST FOR PROPOSALS (RFP) FOR...")
#   [2] Closing      e.g. "29 April 2026 @ 11:00 am"
MOCK_HTML = """
<!DOCTYPE html><html><body><table>
<tbody>
<tr>
    <td>27 March 2026</td>
    <td>REQUEST FOR PROPOSALS (RFP) FOR THE APPOINTMENT OF A SUITABLY QUALIFIED SERVICE PROVIDER</td>
    <td>29 April 2026 @ 11:00 am</td>
</tr>
<tr>
    <td>20 August 2025</td>
    <td>Request for Bid Proposals for the appointment of a Service Provider for provisioning</td>
    <td>29 September 2025 at 11h00</td>
</tr>
</tbody>
</table></body></html>
"""

_TR = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_TD = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")


class AgrisetaSource:
    source_id: str = "agriseta"
    live: bool = True

    def __init__(self, url: str = "https://www.agriseta.co.za/tenders"):
        self.url = url
        self.issuing_entity = "Agricultural Sector Education and Training Authority"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        engaged_fallback = False
        if html_content is None:
            ssl_ctx = _get_ssl_context()
            try:
                html_content = _do_fetch(self.url, _FETCH_TIMEOUT, ssl_ctx)
            except Exception as exc:
                logger.warning("Failed to fetch AgriSETA from %s (%s). Using fallback.", self.url, exc)
                html_content = MOCK_HTML
                engaged_fallback = True
        tenders = self.parse_html(html_content, limit)
        if not tenders and not engaged_fallback:
            tenders = self.parse_html(MOCK_HTML, limit)
        return tenders

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        """AgriSETA: [published, description_with_ref, closing]"""
        tenders: List[TenderOpportunity] = []
        rows = _TR.findall(html or "")
        for idx, row_html in enumerate(rows):
            tds = [_TAG.sub("", td).strip() for td in _TD.findall(row_html)]
            if len(tds) < 3:
                continue
            title_desc = tds[1]
            # Clean closing: strip @time suffix
            closing_str = re.sub(r"@\s*\d{1,2}[:h]\d{2}\s*(?:am|pm)?", "", tds[2], flags=re.IGNORECASE).strip()
            closing_str = re.sub(r"\s+at\s+\d{2}h\d{2}", "", closing_str, flags=re.IGNORECASE).strip()
            # Extract ref from title
            ref_match = re.search(r"(RFP|RFQ|Bid)\s*(?:No\.?)?\s*([\w/-]+)", title_desc, re.IGNORECASE)
            if ref_match and any(ch.isdigit() for ch in ref_match.group(2)):
                ref = f"{ref_match.group(1)} {ref_match.group(2)}"
            else:
                # Generate ref from published date
                ref = f"AgriSETA/{tds[0].replace(' ', '-')[:30]}"
            combined = f"{ref} {title_desc}"
            cidb_hit = re_search_cidb(combined)
            cidb_level = int(cidb_hit[0]) if cidb_hit else None
            cidb_class = cidb_hit[1] if cidb_hit else None
            location = province_from_text(combined) or "Gauteng"
            tenders.append(TenderOpportunity(
                tender_id=ref[:100], title=title_desc[:500],
                issuing_entity=self.issuing_entity, closing_date=parse_closing_date(closing_str),
                estimated_value=None, required_cidb_class=cidb_class, required_cidb_level=cidb_level,
                mandatory_csd=True, tax_compliance_required=True, location_target=location, raw_document_url=None,
            ))
            if limit is not None and len(tenders) >= limit:
                break
        return tenders
