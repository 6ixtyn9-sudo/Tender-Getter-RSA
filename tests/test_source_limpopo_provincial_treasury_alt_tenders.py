"""Tests for the LP Treasury (alt) tender source plug-in."""
import pytest


def test_limpopo_provincial_treasury_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.limpopo_provincial_treasury_alt_tenders import LimpopoProvincialTreasuryAltSource
    src = LimpopoProvincialTreasuryAltSource()
    assert src.source_id == "limpopo_provincial_treasury_alt_tenders"
    assert src.live is True


def test_limpopo_provincial_treasury_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.limpopo_provincial_treasury_alt_tenders import LimpopoProvincialTreasuryAltSource, MOCK_HTML
    src = LimpopoProvincialTreasuryAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_limpopo_provincial_treasury_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.limpopo_provincial_treasury_alt_tenders import LimpopoProvincialTreasuryAltSource
    src = LimpopoProvincialTreasuryAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
