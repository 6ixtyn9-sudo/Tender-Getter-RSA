"""Tender source plug-ins – Racket-Factory style."""
from typing import Protocol, List, runtime_checkable, Dict, Any
from pathlib import Path
import logging

from ..schemas import TenderOpportunity

logger = logging.getLogger(__name__)

@runtime_checkable
class TenderSource(Protocol):
    source_id: str
    def fetch(self, limit: int | None = None) -> List[TenderOpportunity]: ...

# Re-export the built-in parsers / syncers
from .etenders_ocds import sync_live_tenders, parse_ocds_release_to_tender
from .etenders_csv import sync_csv_tenders, parse_csv_row_to_tender
from .common import re_search_cidb, province_from_text

def load_sources() -> List[Dict[str, Any]]:
    """Load src/tender_getter/sources.yaml – returns [] if PyYAML missing."""
    try:
        import yaml  # type: ignore
    except ImportError:
        logger.warning("PyYAML not installed – load_sources() returning empty list")
        return []
    sources_path = Path(__file__).parent.parent / "sources.yaml"
    if not sources_path.exists():
        return []
    with sources_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("sources", []) if isinstance(data, dict) else []

__all__ = [
    "TenderSource",
    "sync_live_tenders", "parse_ocds_release_to_tender",
    "sync_csv_tenders", "parse_csv_row_to_tender",
    "re_search_cidb", "province_from_text",
    "load_sources",
]
