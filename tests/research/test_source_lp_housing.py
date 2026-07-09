"""Tests for the Limpopo Housing tender source plug-in."""
import pytest


def test_lp_housing_source_initialization():
    from tender_getter.sources.research.lp_housing import LpHousingSource
    src = LpHousingSource()
    assert src.source_id == "lp_housing"
    assert isinstance(src.live, bool)


def test_lp_housing_parse_mock_html():
    from tender_getter.sources.research.lp_housing import LpHousingSource, MOCK_HTML
    src = LpHousingSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lp_housing_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.lp_housing import LpHousingSource
    src = LpHousingSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
