"""Tests for the AfDB (SA rep) tender source plug-in."""
import pytest


def test_afdb_source_initialization():
    from tender_getter.sources.research.afdb import AfdbSource
    src = AfdbSource()
    assert src.source_id == "afdb"
    assert isinstance(src.live, bool)


def test_afdb_parse_mock_html():
    from tender_getter.sources.research.afdb import AfdbSource, MOCK_HTML
    src = AfdbSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_afdb_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.afdb import AfdbSource
    src = AfdbSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
