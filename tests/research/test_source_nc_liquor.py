"""Tests for the Northern Cape Liquor Board tender source plug-in."""
import pytest


def test_nc_liquor_source_initialization():
    from tender_getter.sources.research.nc_liquor import NcLiquorSource
    src = NcLiquorSource()
    assert src.source_id == "nc_liquor"
    assert src.live is False


def test_nc_liquor_parse_mock_html():
    from tender_getter.sources.research.nc_liquor import NcLiquorSource, MOCK_HTML
    src = NcLiquorSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nc_liquor_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nc_liquor import NcLiquorSource
    src = NcLiquorSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
