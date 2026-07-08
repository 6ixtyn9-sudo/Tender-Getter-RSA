"""Tests for the Overberg Water tender source plug-in."""
import pytest


def test_overberg_water_tenders_source_initialization():
    from tender_getter.sources.research_extra.overberg_water_tenders import OverbergWaterSource
    src = OverbergWaterSource()
    assert src.source_id == "overberg_water_tenders"
    assert src.live is True


def test_overberg_water_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.overberg_water_tenders import OverbergWaterSource, MOCK_HTML
    src = OverbergWaterSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_overberg_water_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.overberg_water_tenders import OverbergWaterSource
    src = OverbergWaterSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
