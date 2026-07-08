"""
source_sync.py – compatibility shim

Pre-0.3 code imported from here directly:
  from tender_getter.source_sync import re_search_cidb, province_from_text,
      parse_ocds_release_to_tender, sync_live_tenders, ...

As of 0.3 the implementations live in:
  tender_getter.sources.common
  tender_getter.sources.etenders_ocds
  tender_getter.sources.etenders_csv

This module re-exports everything for backwards compatibility with existing tests.
New code should import from tender_getter.sources import ...
"""

# Re-export public API – keeps all 59 existing tests green
from .sources.common import re_search_cidb, province_from_text
from .sources.national.etenders_ocds import parse_ocds_release_to_tender, sync_live_tenders
from .sources.national.etenders_csv import parse_csv_row_to_tender, sync_csv
from .sources import load_sources

__all__ = [
    "re_search_cidb",
    "province_from_text",
    "parse_ocds_release_to_tender",
    "sync_live_tenders",
    "parse_csv_row_to_tender",
    "sync_csv",
    "load_sources",
]
