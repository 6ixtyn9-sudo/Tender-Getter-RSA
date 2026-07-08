"""Tests for the Iziko (alt URL) tender source plug-in."""
import pytest


def test_iziko_alt_tenders_source_initialization():
    from tender_getter.sources.research_extra.iziko_alt_tenders import IzikoAltSource
    src = IzikoAltSource()
    assert src.source_id == "iziko_alt_tenders"
    assert src.live is True


def test_iziko_alt_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.iziko_alt_tenders import IzikoAltSource, MOCK_HTML
    src = IzikoAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_iziko_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.iziko_alt_tenders import IzikoAltSource
    src = IzikoAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
