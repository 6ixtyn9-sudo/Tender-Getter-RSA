"""Tests for the uMngeni-uThukela Water (merged: Umgeni + Mhlathuze) tender source plug-in."""
import pytest


def test_umngeni_uthukela_water_source_initialization():
    from tender_getter.sources.water.umngeni_uthukela_water import UmngeniUthukelaWaterSource
    src = UmngeniUthukelaWaterSource()
    assert src.source_id == "umngeni_uthukela_water"
    assert src.live is True


def test_umngeni_uthukela_water_parse_mock_html():
    from tender_getter.sources.water.umngeni_uthukela_water import UmngeniUthukelaWaterSource, MOCK_HTML
    src = UmngeniUthukelaWaterSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umngeni_uthukela_water_fetch_uses_fallback_on_empty():
    from tender_getter.sources.water.umngeni_uthukela_water import UmngeniUthukelaWaterSource
    src = UmngeniUthukelaWaterSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
