"""Tanzania Communications Regulatory Authority – WordPress API source."""
import logging
from typing import List, Optional
from ...schemas import TenderOpportunity
from ..wp_api import wp_fetch_tenders

logger = logging.getLogger(__name__)


class TctaSource:
    source_id: str = "tcta"
    live: bool = True

    def __init__(self):
        self.url = "https://www.tcta.co.za"
        self.issuing_entity = "Trans-Caledon Tunnel Authority"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        return wp_fetch_tenders(
            source_id=self.source_id,
            url=self.url,
            post_type="tcta-tenders",
            issuing_entity=self.issuing_entity,
            default_location="Gauteng",
            limit=limit,
        )

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        return []
