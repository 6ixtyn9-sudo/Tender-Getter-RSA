"""Tests for the SEDA (alt) tender source plug-in."""
import pytest


def test_seda_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.seda_alt_tenders import SedaAltSource
    src = SedaAltSource()
    assert src.source_id == "seda_alt_tenders"
    assert src.live is True


def test_seda_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.seda_alt_tenders import SedaAltSource, MOCK_HTML
    src = SedaAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_seda_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.seda_alt_tenders import SedaAltSource
    src = SedaAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
