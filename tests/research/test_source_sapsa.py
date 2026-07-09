"""Tests for the South African Police Service Act (admin) tender source plug-in."""
import pytest


def test_sapsa_source_initialization():
    from tender_getter.sources.research.sapsa import SapsaSource
    src = SapsaSource()
    assert src.source_id == "sapsa"
    assert isinstance(src.live, bool)


def test_sapsa_parse_mock_html():
    from tender_getter.sources.research.sapsa import SapsaSource, MOCK_HTML
    src = SapsaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sapsa_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.sapsa import SapsaSource
    src = SapsaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
