"""Tests for the National Youth Development Agency (NYDA) tender source plug-in."""
import pytest


def test_nyda_tenders_source_initialization():
    from tender_getter.sources.schedule3a.nyda_tenders import NydaSource
    src = NydaSource()
    assert src.source_id == "nyda_tenders"
    assert src.live is True


def test_nyda_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.nyda_tenders import NydaSource, MOCK_HTML
    src = NydaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nyda_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.nyda_tenders import NydaSource
    src = NydaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
