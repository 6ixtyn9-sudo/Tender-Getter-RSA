"""Tests for the Northern Cape Tourism Authority tender source plug-in."""
import pytest


def test_nc_tourism_source_initialization():
    from tender_getter.sources.research.nc_tourism import NcTourismSource
    src = NcTourismSource()
    assert src.source_id == "nc_tourism"
    assert src.live is False


def test_nc_tourism_parse_mock_html():
    from tender_getter.sources.research.nc_tourism import NcTourismSource, MOCK_HTML
    src = NcTourismSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nc_tourism_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nc_tourism import NcTourismSource
    src = NcTourismSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
