"""Tests for the Northern Cape Agriculture tender source plug-in."""
import pytest


def test_nc_agriculture_tenders_source_initialization():
    from tender_getter.sources.research_extra.nc_agriculture_tenders import NcAgricultureSource
    src = NcAgricultureSource()
    assert src.source_id == "nc_agriculture_tenders"
    assert src.live is False


def test_nc_agriculture_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.nc_agriculture_tenders import NcAgricultureSource, MOCK_HTML
    src = NcAgricultureSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nc_agriculture_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.nc_agriculture_tenders import NcAgricultureSource
    src = NcAgricultureSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
