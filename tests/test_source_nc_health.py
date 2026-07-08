"""Tests for the Northern Cape Health tender source plug-in."""
import pytest


def test_nc_health_source_initialization():
    from tender_getter.sources.research.nc_health import NcHealthSource
    src = NcHealthSource()
    assert src.source_id == "nc_health"
    assert src.live is True


def test_nc_health_parse_mock_html():
    from tender_getter.sources.research.nc_health import NcHealthSource, MOCK_HTML
    src = NcHealthSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nc_health_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nc_health import NcHealthSource
    src = NcHealthSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
