"""Tests for the Northern Cape Parks tender source plug-in."""
import pytest


def test_nc_parks_tenders_source_initialization():
    from tender_getter.sources.research_extra.nc_parks_tenders import NcParksSource
    src = NcParksSource()
    assert src.source_id == "nc_parks_tenders"
    assert src.live is False


def test_nc_parks_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.nc_parks_tenders import NcParksSource, MOCK_HTML
    src = NcParksSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nc_parks_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.nc_parks_tenders import NcParksSource
    src = NcParksSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
