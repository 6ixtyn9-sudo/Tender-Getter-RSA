"""Tender source plug-ins.

Architecture (v2.2.0):
  - sources.yaml is the registry metadata (845 entries).
  - Each entry has its own per-source Python file under
    sources/<category>/<entity_id>.py, exposing one TenderSource class.
  - Each source file has its own MOCK_HTML constant and its own test in
    tests/test_source_<entity_id>.py.
  - Adding a new source = create one Python file + one test file +
    add one YAML entry. Grep-friendly, diff-friendly, debuggable.
  - Bespoke plug-ins (eTenders OCDS API, eTenders CSV, CIDB) live in
    sources/national/ and have unique parsers.
"""
from typing import Protocol, List, runtime_checkable, Dict, Any
from pathlib import Path
import logging

from ..schemas import TenderOpportunity

logger = logging.getLogger(__name__)


@runtime_checkable
class TenderSource(Protocol):
    source_id: str
    def fetch(self, limit: int | None = None) -> List[TenderOpportunity]: ...


# Unique-parser plug-ins are explicitly imported for clarity
from .national.etenders_ocds import sync_live_tenders, parse_ocds_release_to_tender
from .national.etenders_csv import sync_csv_tenders, parse_csv_row_to_tender
from .national.cidb import CIDBSource

# Shared parsing utilities
from .generic import standard_fetch, parse_html_table
from .common import re_search_cidb, province_from_text


def load_sources() -> List[Dict[str, Any]]:
    """Load src/tender_getter/sources.yaml – returns [] if PyYAML missing."""
    try:
        import yaml
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
    "sync_live_tenders",
    "parse_ocds_release_to_tender",
    "sync_csv_tenders",
    "parse_csv_row_to_tender",
    "CIDBSource",
    "standard_fetch",
    "parse_html_table",
    "re_search_cidb",
    "province_from_text",
    "load_sources",
]
