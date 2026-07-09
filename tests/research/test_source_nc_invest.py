"""Tests for the Northern Cape Investment tender source plug-in."""
import pytest


def test_nc_invest_source_initialization():
    from tender_getter.sources.research.nc_invest import NcInvestSource
    src = NcInvestSource()
    assert src.source_id == "nc_invest"
    assert isinstance(src.live, bool)


def test_nc_invest_parse_mock_html():
    from tender_getter.sources.research.nc_invest import NcInvestSource, MOCK_HTML
    src = NcInvestSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nc_invest_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nc_invest import NcInvestSource
    src = NcInvestSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
