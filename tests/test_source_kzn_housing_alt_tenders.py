"""Tests for the KZN Housing (alt) tender source plug-in."""
import pytest


def test_kzn_housing_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.kzn_housing_alt_tenders import KznHousingAltSource
    src = KznHousingAltSource()
    assert src.source_id == "kzn_housing_alt_tenders"
    assert src.live is True


def test_kzn_housing_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.kzn_housing_alt_tenders import KznHousingAltSource, MOCK_HTML
    src = KznHousingAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kzn_housing_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.kzn_housing_alt_tenders import KznHousingAltSource
    src = KznHousingAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
