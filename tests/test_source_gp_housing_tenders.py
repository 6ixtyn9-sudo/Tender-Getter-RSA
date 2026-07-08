"""Tests for the Gauteng Housing Board tender source plug-in."""
import pytest


def test_gp_housing_tenders_source_initialization():
    from tender_getter.sources.research_extra.gp_housing_tenders import GpHousingSource
    src = GpHousingSource()
    assert src.source_id == "gp_housing_tenders"
    assert src.live is False


def test_gp_housing_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.gp_housing_tenders import GpHousingSource, MOCK_HTML
    src = GpHousingSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gp_housing_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.gp_housing_tenders import GpHousingSource
    src = GpHousingSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
