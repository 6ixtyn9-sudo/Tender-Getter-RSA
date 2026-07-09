"""Ugu District Municipality – WordPress API source."""
import logging
from typing import List, Optional
from ...schemas import TenderOpportunity
from ..wp_api import wp_fetch_tenders

logger = logging.getLogger(__name__)


class UguDmSource:
    source_id: str = "ugu_dm"
    live: bool = True

    def __init__(self):
        self.url = "https://www.ugu.gov.za"
        self.issuing_entity = "Ugu District Municipality"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        return wp_fetch_tenders(
            source_id=self.source_id,
            url=self.url,
            post_type="tender",
            issuing_entity=self.issuing_entity,
            default_location="KwaZulu-Natal",
            limit=limit,
        )

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        return []
