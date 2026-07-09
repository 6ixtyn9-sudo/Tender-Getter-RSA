"""Tests for the City Power Johannesburg tender source plug-in."""
import pytest


def test_coj_city_power_source_initialization():
    from tender_getter.sources.local_municipalities.coj_city_power import CojCityPowerSource
    src = CojCityPowerSource()
    assert src.source_id == "coj_city_power"
    assert isinstance(src.live, bool)


def test_coj_city_power_parse_mock_html():
    from tender_getter.sources.local_municipalities.coj_city_power import CojCityPowerSource, MOCK_HTML
    src = CojCityPowerSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_coj_city_power_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.coj_city_power import CojCityPowerSource
    src = CojCityPowerSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
