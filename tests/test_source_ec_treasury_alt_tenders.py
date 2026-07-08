"""Tests for the EC Treasury (alt URL) tender source plug-in."""
import pytest


def test_ec_treasury_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.ec_treasury_alt_tenders import EcTreasuryAltSource
    src = EcTreasuryAltSource()
    assert src.source_id == "ec_treasury_alt_tenders"
    assert src.live is True


def test_ec_treasury_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.ec_treasury_alt_tenders import EcTreasuryAltSource, MOCK_HTML
    src = EcTreasuryAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ec_treasury_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.ec_treasury_alt_tenders import EcTreasuryAltSource
    src = EcTreasuryAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
