"""Tests for the Northern Cape Investment tender source plug-in."""
import pytest


def test_nc_invest_tenders_source_initialization():
    from tender_getter.sources.research_extra.nc_invest_tenders import NcInvestSource
    src = NcInvestSource()
    assert src.source_id == "nc_invest_tenders"
    assert src.live is False


def test_nc_invest_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.nc_invest_tenders import NcInvestSource, MOCK_HTML
    src = NcInvestSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nc_invest_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.nc_invest_tenders import NcInvestSource
    src = NcInvestSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
