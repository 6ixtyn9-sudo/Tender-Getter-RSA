"""Tests for the North West Housing Board tender source plug-in."""
import pytest


def test_nw_housing_source_initialization():
    from tender_getter.sources.research.nw_housing import NwHousingSource
    src = NwHousingSource()
    assert src.source_id == "nw_housing"
    assert src.live is False


def test_nw_housing_parse_mock_html():
    from tender_getter.sources.research.nw_housing import NwHousingSource, MOCK_HTML
    src = NwHousingSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nw_housing_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nw_housing import NwHousingSource
    src = NwHousingSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
