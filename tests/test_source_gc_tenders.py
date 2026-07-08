"""Tests for the Gauteng Convention Bureau tender source plug-in."""
import pytest


def test_gc_tenders_source_initialization():
    from tender_getter.sources.research_extra.gc_tenders import GcSource
    src = GcSource()
    assert src.source_id == "gc_tenders"
    assert src.live is False


def test_gc_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.gc_tenders import GcSource, MOCK_HTML
    src = GcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gc_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.gc_tenders import GcSource
    src = GcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
