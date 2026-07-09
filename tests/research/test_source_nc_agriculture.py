"""Tests for the Northern Cape Agriculture tender source plug-in."""
import pytest


def test_nc_agriculture_source_initialization():
    from tender_getter.sources.research.nc_agriculture import NcAgricultureSource
    src = NcAgricultureSource()
    assert src.source_id == "nc_agriculture"
    assert isinstance(src.live, bool)


def test_nc_agriculture_parse_mock_html():
    from tender_getter.sources.research.nc_agriculture import NcAgricultureSource, MOCK_HTML
    src = NcAgricultureSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nc_agriculture_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nc_agriculture import NcAgricultureSource
    src = NcAgricultureSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
