"""Tests for the Rand Water tender source plug-in."""
import pytest


def test_rand_water_tenders_source_initialization():
    from tender_getter.sources.research_extra.rand_water_tenders import RandWaterSource
    src = RandWaterSource()
    assert src.source_id == "rand_water_tenders"
    assert src.live is True


def test_rand_water_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.rand_water_tenders import RandWaterSource, MOCK_HTML
    src = RandWaterSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_rand_water_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.rand_water_tenders import RandWaterSource
    src = RandWaterSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
