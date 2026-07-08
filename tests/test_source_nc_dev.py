"""Tests for the Northern Cape Economic Development Agency tender source plug-in."""
import pytest


def test_nc_dev_source_initialization():
    from tender_getter.sources.research.nc_dev import NcDevSource
    src = NcDevSource()
    assert src.source_id == "nc_dev"
    assert src.live is False


def test_nc_dev_parse_mock_html():
    from tender_getter.sources.research.nc_dev import NcDevSource, MOCK_HTML
    src = NcDevSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nc_dev_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nc_dev import NcDevSource
    src = NcDevSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
