"""Tests for the National Youth Development Agency (NYDA) tender source plug-in."""
import pytest


def test_nyda_source_initialization():
    from tender_getter.sources.schedule3a.nyda import NydaSource
    src = NydaSource()
    assert src.source_id == "nyda"
    assert isinstance(src.live, bool)


def test_nyda_parse_mock_html():
    from tender_getter.sources.schedule3a.nyda import NydaSource, MOCK_HTML
    src = NydaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nyda_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.nyda import NydaSource
    src = NydaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
