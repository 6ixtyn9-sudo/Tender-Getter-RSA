"""Tests for the National Health Research Ethics Council tender source plug-in."""
import pytest


def test_nhrsc_source_initialization():
    from tender_getter.sources.research.nhrsc import NhrscSource
    src = NhrscSource()
    assert src.source_id == "nhrsc"
    assert src.live is False


def test_nhrsc_parse_mock_html():
    from tender_getter.sources.research.nhrsc import NhrscSource, MOCK_HTML
    src = NhrscSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nhrsc_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nhrsc import NhrscSource
    src = NhrscSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
