"""Tests for the National Health Research Ethics Council tender source plug-in."""
import pytest


def test_nhrsc_tenders_source_initialization():
    from tender_getter.sources.research_extra.nhrsc_tenders import NhrscSource
    src = NhrscSource()
    assert src.source_id == "nhrsc_tenders"
    assert src.live is False


def test_nhrsc_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.nhrsc_tenders import NhrscSource, MOCK_HTML
    src = NhrscSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nhrsc_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.nhrsc_tenders import NhrscSource
    src = NhrscSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
