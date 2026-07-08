"""Tests for the Sedibeng Water (legacy – merged into Vaal Central) tender source plug-in."""
import pytest


def test_sedibeng_water_tenders_source_initialization():
    from tender_getter.sources.research_extra.sedibeng_water_tenders import SedibengWaterSource
    src = SedibengWaterSource()
    assert src.source_id == "sedibeng_water_tenders"
    assert src.live is False


def test_sedibeng_water_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.sedibeng_water_tenders import SedibengWaterSource, MOCK_HTML
    src = SedibengWaterSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sedibeng_water_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.sedibeng_water_tenders import SedibengWaterSource
    src = SedibengWaterSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
