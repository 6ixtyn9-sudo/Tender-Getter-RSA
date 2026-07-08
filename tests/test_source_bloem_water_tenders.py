"""Tests for the Bloem Water (legacy – merged into Vaal Central) tender source plug-in."""
import pytest


def test_bloem_water_tenders_source_initialization():
    from tender_getter.sources.research_extra.bloem_water_tenders import BloemWaterSource
    src = BloemWaterSource()
    assert src.source_id == "bloem_water_tenders"
    assert src.live is False


def test_bloem_water_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.bloem_water_tenders import BloemWaterSource, MOCK_HTML
    src = BloemWaterSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_bloem_water_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.bloem_water_tenders import BloemWaterSource
    src = BloemWaterSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
