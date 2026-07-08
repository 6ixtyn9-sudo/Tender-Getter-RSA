"""Tests for the City of Tshwane Water and Sanitation Division tender source plug-in."""
import pytest


def test_tshwane_water_source_initialization():
    from tender_getter.sources.water.tshwane_water import TshwaneWaterSource
    src = TshwaneWaterSource()
    assert src.source_id == "tshwane_water"
    assert src.live is True


def test_tshwane_water_parse_mock_html():
    from tender_getter.sources.water.tshwane_water import TshwaneWaterSource, MOCK_HTML
    src = TshwaneWaterSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_tshwane_water_fetch_uses_fallback_on_empty():
    from tender_getter.sources.water.tshwane_water import TshwaneWaterSource
    src = TshwaneWaterSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
