"""Tests for the Gauteng Convention Bureau tender source plug-in."""
import pytest


def test_gc_source_initialization():
    from tender_getter.sources.research.gc import GcSource
    src = GcSource()
    assert src.source_id == "gc"
    assert isinstance(src.live, bool)


def test_gc_parse_mock_html():
    from tender_getter.sources.research.gc import GcSource, MOCK_HTML
    src = GcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gc_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.gc import GcSource
    src = GcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
