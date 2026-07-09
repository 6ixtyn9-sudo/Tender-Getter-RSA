"""George Municipality – WordPress API source."""
import logging
from typing import List, Optional
from ...schemas import TenderOpportunity
from ..wp_api import wp_fetch_tenders

logger = logging.getLogger(__name__)


class GeorgeLmSource:
    source_id: str = "george_lm"
    live: bool = True

    def __init__(self):
        self.url = "https://www.george.gov.za"
        self.issuing_entity = "George Municipality"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        return wp_fetch_tenders(
            source_id=self.source_id,
            url=self.url,
            post_type="supply-chain-categor",
            issuing_entity=self.issuing_entity,
            default_location="Western Cape",
            limit=limit,
        )

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        return []
