"""South African Revenue Service – WordPress API source for awarded tenders."""
import logging
from typing import List, Optional
from ...schemas import TenderOpportunity
from ..wp_api import wp_fetch_tenders

logger = logging.getLogger(__name__)


class SarsSource:
    source_id: str = "sars"
    live: bool = True

    def __init__(self):
        self.url = "https://www.sars.gov.za"
        self.issuing_entity = "South African Revenue Service"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        return wp_fetch_tenders(
            source_id=self.source_id,
            url=self.url,
            post_type="awarded_tender",
            issuing_entity=self.issuing_entity,
            default_location="Gauteng",
            limit=limit,
        )

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        return []
