"""Tests for the Magalies Water tender source plug-in."""
import pytest


def test_magalies_water_tenders_source_initialization():
    from tender_getter.sources.research_extra.magalies_water_tenders import MagaliesWaterSource
    src = MagaliesWaterSource()
    assert src.source_id == "magalies_water_tenders"
    assert src.live is True


def test_magalies_water_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.magalies_water_tenders import MagaliesWaterSource, MOCK_HTML
    src = MagaliesWaterSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_magalies_water_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.magalies_water_tenders import MagaliesWaterSource
    src = MagaliesWaterSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
