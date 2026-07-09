"""Tests for the Government Communication and Information System (GCIS) tender source plug-in."""
import pytest


def test_gcis_source_initialization():
    from tender_getter.sources.schedule3a.gcis import GcisSource
    src = GcisSource()
    assert src.source_id == "gcis"
    assert isinstance(src.live, bool)


def test_gcis_parse_mock_html():
    from tender_getter.sources.schedule3a.gcis import GcisSource, MOCK_HTML
    src = GcisSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gcis_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.gcis import GcisSource
    src = GcisSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
