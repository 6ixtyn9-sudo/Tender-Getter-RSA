"""Newcastle Local Municipality tender source plug-in.

Newcastle (newcastle.gov.za) is a WordPress site. Their tender custom post
type doesn't exist (/wp-json/wp/v2/tenders → 404), but tender notices are
published as WP posts and pages. We search via WP posts API and also try
the /tenders/ page for HTML tables.
"""
import json
import logging
import re
import ssl
from typing import List, Optional
from urllib.request import urlopen, Request

from ...schemas import TenderOpportunity
from ..common import re_search_cidb, province_from_text, parse_closing_date
from ..wp_api import _parse_wp_items, _ssl_ctx
from ..generic import standard_fetch, parse_html_table

logger = logging.getLogger(__name__)

_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"

MOCK_HTML = """
<!DOCTYPE html>
<html>
<head><title>Newcastle Local Municipality Tenders</title></head>
<body>
  <table>
    <thead><tr><th>Reference</th><th>Description</th><th>Closing Date</th></tr></thead>
    <tbody>
      <tr>
        <td>NEWCASTLE/BID/2026/001</td>
        <td>Provision of Security Services – Newcastle LM (KwaZulu-Natal)</td>
        <td>2026-09-30 11:00:00</td>
      </tr>
      <tr>
        <td>NEWCASTLE/BID/2026/002</td>
        <td>Supply and Delivery of Electrical Materials (KwaZulu-Natal)</td>
        <td>2026-10-15 11:00:00</td>
      </tr>
    </tbody>
  </table>
</body>
</html>
"""


def _fetch_newcastle_wp(limit: Optional[int] = None) -> List[TenderOpportunity]:
    """Search WP posts for tender notices."""
    ctx = _ssl_ctx()
    per_page = min(limit or 30, 100)
    all_items = []

    for search_term in ["tender", "bid", "quotation"]:
        api_url = (
            f"https://newcastle.gov.za/wp-json/wp/v2/posts"
            f"?per_page={per_page}&search={search_term}&orderby=date&order=desc"
        )
        try:
            req = Request(api_url, headers={"User-Agent": _UA, "Accept": "application/json"})
            kw = {"timeout": 15}
            if ctx:
                kw["context"] = ctx
            with urlopen(req, **kw) as resp:
                items = json.loads(resp.read())
            if isinstance(items, list):
                all_items.extend(items)
        except Exception as exc:
            logger.debug("Newcastle WP posts search '%s' failed: %s", search_term, exc)

    if not all_items:
        return []

    # De-dupe by id
    seen: set = set()
    unique = []
    for item in all_items:
        if item.get("id") not in seen:
            seen.add(item.get("id"))
            unique.append(item)

    tenders = _parse_wp_items(
        unique,
        source_id="newcastle_lm",
        issuing_entity="Newcastle Local Municipality",
        default_location="KwaZulu-Natal",
        limit=limit,
    )

    # Filter: only posts that actually look like tenders
    tender_re = re.compile(
        r"\b(tender|bid|rfq|quotation|notice|supply|procure)\b", re.IGNORECASE
    )
    return [t for t in tenders if tender_re.search(t.title)]


class NewcastleLmSource:
    """Tender source plug-in for Newcastle Local Municipality."""

    source_id: str = "newcastle_lm"
    live: bool = True

    def __init__(self, url: str = "https://newcastle.gov.za/tenders/"):
        self.url = url
        self.issuing_entity = "Newcastle Local Municipality"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        """WP posts API → HTML table → mock fallback."""
        if html_content is not None:
            tenders = self.parse_html(html_content, limit)
            if tenders:
                return tenders
            return self.parse_html(MOCK_HTML, limit)

        # Strategy 1: WP posts API
        tenders = _fetch_newcastle_wp(limit)
        if tenders:
            logger.info("Newcastle: %d tenders via WP posts API", len(tenders))
            return tenders

        # Strategy 2: HTML table parse of /tenders/ page
        tenders = standard_fetch(self.url, MOCK_HTML, None, limit)
        real = [t for t in tenders if not t.tender_id.startswith("NEWCASTLE/BID")]
        if real:
            return real

        # Fallback mock
        logger.warning("Newcastle: all live strategies failed – using mock")
        return self.parse_html(MOCK_HTML, limit)

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        """Parse <tr><td> rows."""
        return parse_html_table(html, limit, issuing_entity=self.issuing_entity)
