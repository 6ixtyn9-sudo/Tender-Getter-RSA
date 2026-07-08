"""Tests for the Vaal Central Water (merged: Bloem + Sedibeng + Lepelle) tender source plug-in."""
import pytest


def test_vaal_central_water_tenders_source_initialization():
    from tender_getter.sources.research_extra.vaal_central_water_tenders import VaalCentralWaterSource
    src = VaalCentralWaterSource()
    assert src.source_id == "vaal_central_water_tenders"
    assert src.live is True


def test_vaal_central_water_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.vaal_central_water_tenders import VaalCentralWaterSource, MOCK_HTML
    src = VaalCentralWaterSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_vaal_central_water_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.vaal_central_water_tenders import VaalCentralWaterSource
    src = VaalCentralWaterSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
