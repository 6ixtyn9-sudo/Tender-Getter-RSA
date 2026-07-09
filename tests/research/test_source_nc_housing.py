"""Tests for the Northern Cape Housing tender source plug-in."""
import pytest


def test_nc_housing_source_initialization():
    from tender_getter.sources.research.nc_housing import NcHousingSource
    src = NcHousingSource()
    assert src.source_id == "nc_housing"
    assert src.live is False


def test_nc_housing_parse_mock_html():
    from tender_getter.sources.research.nc_housing import NcHousingSource, MOCK_HTML
    src = NcHousingSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nc_housing_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nc_housing import NcHousingSource
    src = NcHousingSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
