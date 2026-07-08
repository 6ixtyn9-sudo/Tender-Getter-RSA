"""Tests for the NPA (alt) tender source plug-in."""
import pytest


def test_npa_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.npa_alt_tenders import NpaAltSource
    src = NpaAltSource()
    assert src.source_id == "npa_alt_tenders"
    assert src.live is True


def test_npa_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.npa_alt_tenders import NpaAltSource, MOCK_HTML
    src = NpaAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_npa_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.npa_alt_tenders import NpaAltSource
    src = NpaAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
