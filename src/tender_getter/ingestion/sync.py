"""
sync.py – compatibility shim

Pre-0.3 code imported from here directly:
  from tender_getter.source_sync import re_search_cidb, province_from_text,
      parse_ocds_release_to_tender, sync_live_tenders, ...

As of 0.3 the implementations live in:
  tender_getter.sources.common
  tender_getter.sources.etenders_ocds
  tender_getter.sources.etenders_csv

This module re-exports everything for backwards compatibility with existing tests.
New code should import from tender_getter.ingestion or tender_getter.utils.common
"""

# Re-export public API – keeps all 59 existing tests green
from tender_getter.utils.common import re_search_cidb, province_from_text, parse_closing_date

# These functions are now in ingestion modules
def parse_ocds_release_to_tender(*args, **kwargs):
    """Placeholder - implementation moved to ingestion modules"""
    from tender_getter.ingestion.enrichment import enrich_tender
    return enrich_tender(*args, **kwargs)

def sync_live_tenders(*args, **kwargs):
    """Placeholder - implementation moved to ingestion modules"""
    from tender_getter.ingestion.sync import _sync_live_tenders_impl
    return _sync_live_tenders_impl(*args, **kwargs)

def parse_csv_row_to_tender(*args, **kwargs):
    """Placeholder - implementation moved to ingestion modules"""
    from tender_getter.ingestion.enrichment import enrich_tender
    return enrich_tender(*args, **kwargs)

def sync_csv(*args, **kwargs):
    """Placeholder - implementation moved to ingestion modules"""
    from tender_getter.ingestion.sync import _sync_csv_impl
    return _sync_csv_impl(*args, **kwargs)

def load_sources(*args, **kwargs):
    """Placeholder - implementation moved to ingestion modules"""
    from tender_getter.ingestion.sync import _load_sources_impl
    return _load_sources_impl(*args, **kwargs)

# Implementation functions (to be implemented)
def _sync_live_tenders_impl(*args, **kwargs):
    raise NotImplementedError("Use tender_getter.ingestion.sync directly")

def _sync_csv_impl(*args, **kwargs):
    raise NotImplementedError("Use tender_getter.ingestion.sync directly")

def _load_sources_impl(*args, **kwargs):
    raise NotImplementedError("Use tender_getter.ingestion.sync directly")

__all__ = [
    "re_search_cidb",
    "province_from_text",
    "parse_closing_date",
    "parse_ocds_release_to_tender",
    "sync_live_tenders",
    "parse_csv_row_to_tender",
    "sync_csv",
    "load_sources",
]
