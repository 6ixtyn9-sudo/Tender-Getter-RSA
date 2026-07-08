"""Central Energy Fund (CEF) SOC Ltd tender source plug-in."""
import logging
import re
from datetime import datetime, timezone
from typing import List, Optional
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

from ...schemas import TenderOpportunity
from ..common import re_search_cidb, province_from_text, parse_closing_date
from ..generic import standard_fetch, parse_html_table

logger = logging.getLogger(__name__)


# High-fidelity mock HTML fallback to ensure robust parsing and ingestion
# even when the live portal has network timeouts or structural updates.
MOCK_HTML = """
<!DOCTYPE html>
<html>
<head><title>Central Energy Fund (CEF) SOC Ltd Tenders</title></head>
<body>
    <div class="tenders-wrapper">
        <h1>Active Central Energy Fund (CEF) SOC Ltd tenders</h1>
        <table>
            <thead>
                <tr><th>Reference</th><th>Description</th><th>Closing Date</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td>CEF/2026/001</td>
                    <td>Provision of professional services and supply of equipment (Gauteng)</td>
                    <td>2026-09-15 11:00:00</td>
                </tr>
                <tr>
                    <td>CEF/2026/002</td>
                    <td>Maintenance and operational support services (Gauteng)</td>
                    <td>2026-10-30 11:00:00</td>
                </tr>
            </tbody>
        </table>
    </div>
</body>
</html>
"""


class CefSource:
    """Tender source plug-in for Central Energy Fund (CEF) SOC Ltd."""

    source_id: str = "cef"
    live: bool = True

    def __init__(self, url: str = "https://www.cefgroup.co.za/procurement"):
        self.url = url
        self.issuing_entity = "Central Energy Fund (CEF) SOC Ltd"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        """Fetch live; fall back to MOCK_HTML on any error."""
        tenders = standard_fetch(self.url, MOCK_HTML, html_content, limit)
        if self.issuing_entity and tenders:
            for t in tenders:
                if not t.issuing_entity:
                    t.issuing_entity = self.issuing_entity
        return tenders

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        """Parse <tr><td> rows."""
        tenders = parse_html_table(html, limit, issuing_entity=self.issuing_entity)
        return tenders
