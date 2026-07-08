"""Tests for the South African Police Service Act (admin) tender source plug-in."""
import pytest


def test_sapsa_tenders_source_initialization():
    from tender_getter.sources.research_extra.sapsa_tenders import SapsaSource
    src = SapsaSource()
    assert src.source_id == "sapsa_tenders"
    assert src.live is True


def test_sapsa_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.sapsa_tenders import SapsaSource, MOCK_HTML
    src = SapsaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sapsa_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.sapsa_tenders import SapsaSource
    src = SapsaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
