"""Tests for the uMngeni-uThukela Water (merged: Umgeni + Mhlathuze) tender source plug-in."""
import pytest


def test_umngeni_uthukela_water_tenders_source_initialization():
    from tender_getter.sources.research_extra.umngeni_uthukela_water_tenders import UmngeniUthukelaWaterSource
    src = UmngeniUthukelaWaterSource()
    assert src.source_id == "umngeni_uthukela_water_tenders"
    assert src.live is True


def test_umngeni_uthukela_water_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.umngeni_uthukela_water_tenders import UmngeniUthukelaWaterSource, MOCK_HTML
    src = UmngeniUthukelaWaterSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umngeni_uthukela_water_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.umngeni_uthukela_water_tenders import UmngeniUthukelaWaterSource
    src = UmngeniUthukelaWaterSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
