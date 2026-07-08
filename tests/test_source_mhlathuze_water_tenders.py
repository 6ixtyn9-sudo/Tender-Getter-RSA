"""Tests for the Mhlathuze Water (legacy – merged into uMngeni-uThukela) tender source plug-in."""
import pytest


def test_mhlathuze_water_tenders_source_initialization():
    from tender_getter.sources.research_extra.mhlathuze_water_tenders import MhlathuzeWaterSource
    src = MhlathuzeWaterSource()
    assert src.source_id == "mhlathuze_water_tenders"
    assert src.live is False


def test_mhlathuze_water_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.mhlathuze_water_tenders import MhlathuzeWaterSource, MOCK_HTML
    src = MhlathuzeWaterSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mhlathuze_water_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.mhlathuze_water_tenders import MhlathuzeWaterSource
    src = MhlathuzeWaterSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
