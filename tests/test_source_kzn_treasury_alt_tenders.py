"""Tests for the KZN Treasury (alt URL) tender source plug-in."""
import pytest


def test_kzn_treasury_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.kzn_treasury_alt_tenders import KznTreasuryAltSource
    src = KznTreasuryAltSource()
    assert src.source_id == "kzn_treasury_alt_tenders"
    assert src.live is True


def test_kzn_treasury_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.kzn_treasury_alt_tenders import KznTreasuryAltSource, MOCK_HTML
    src = KznTreasuryAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kzn_treasury_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.kzn_treasury_alt_tenders import KznTreasuryAltSource
    src = KznTreasuryAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
