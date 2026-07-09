"""Tests for the Northern Cape Heritage tender source plug-in."""
import pytest


def test_nc_heritage_source_initialization():
    from tender_getter.sources.research.nc_heritage import NcHeritageSource
    src = NcHeritageSource()
    assert src.source_id == "nc_heritage"
    assert src.live is False


def test_nc_heritage_parse_mock_html():
    from tender_getter.sources.research.nc_heritage import NcHeritageSource, MOCK_HTML
    src = NcHeritageSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nc_heritage_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nc_heritage import NcHeritageSource
    src = NcHeritageSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
