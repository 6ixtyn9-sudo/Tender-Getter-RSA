"""Makhado (alt) tender source plug-in."""
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


MOCK_HTML = """
<!DOCTYPE html>
<html>
<head><title>Makhado (alt) Tenders</title></head>
<body>
    <table>
        <tr><th>Reference</th><th>Description</th><th>Closing Date</th></tr>
        <tr><td>MAKHADO_ALT_2_LM/2026/001</td><td>Provision of professional services (Gauteng)</td><td>2026-09-15 11:00:00</td></tr>
        <tr><td>MAKHADO_ALT_2_LM/2026/002</td><td>Maintenance and operational support services (Gauteng)</td><td>2026-10-30 11:00:00</td></tr>
    </table>
</body>
</html>
"""


class MakhadoAlt2LmSource:
    source_id: str = "makhado_alt_2_lm_tenders"
    live: bool = False

    def __init__(self, url: str = "https://www.makhado.gov.za/procurement"):
        self.url = url
        self.issuing_entity = "Makhado (alt)"

    def fetch(self, limit=None, html_content=None):
        tenders = standard_fetch(self.url, MOCK_HTML, html_content, limit)
        if self.issuing_entity and tenders:
            for t in tenders:
                if not t.issuing_entity:
                    t.issuing_entity = self.issuing_entity
        return tenders

    def parse_html(self, html, limit=None):
        return parse_html_table(html, limit, issuing_entity=self.issuing_entity)
