"""Tests for the Lepelle Northern Water (legacy – merged into Vaal Central) tender source plug-in."""
import pytest


def test_lepelle_water_tenders_source_initialization():
    from tender_getter.sources.research_extra.lepelle_water_tenders import LepelleWaterSource
    src = LepelleWaterSource()
    assert src.source_id == "lepelle_water_tenders"
    assert src.live is False


def test_lepelle_water_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.lepelle_water_tenders import LepelleWaterSource, MOCK_HTML
    src = LepelleWaterSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lepelle_water_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.lepelle_water_tenders import LepelleWaterSource
    src = LepelleWaterSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
