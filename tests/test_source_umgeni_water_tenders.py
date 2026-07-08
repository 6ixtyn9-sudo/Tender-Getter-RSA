"""Tests for the Umgeni Water (legacy – merged into uMngeni-uThukela) tender source plug-in."""
import pytest


def test_umgeni_water_tenders_source_initialization():
    from tender_getter.sources.research_extra.umgeni_water_tenders import UmgeniWaterSource
    src = UmgeniWaterSource()
    assert src.source_id == "umgeni_water_tenders"
    assert src.live is False


def test_umgeni_water_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.umgeni_water_tenders import UmgeniWaterSource, MOCK_HTML
    src = UmgeniWaterSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umgeni_water_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.umgeni_water_tenders import UmgeniWaterSource
    src = UmgeniWaterSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
