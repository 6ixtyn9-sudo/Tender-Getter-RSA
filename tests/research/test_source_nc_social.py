"""Tests for the Northern Cape Social Development tender source plug-in."""
import pytest


def test_nc_social_source_initialization():
    from tender_getter.sources.research.nc_social import NcSocialSource
    src = NcSocialSource()
    assert src.source_id == "nc_social"
    assert isinstance(src.live, bool)


def test_nc_social_parse_mock_html():
    from tender_getter.sources.research.nc_social import NcSocialSource, MOCK_HTML
    src = NcSocialSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nc_social_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nc_social import NcSocialSource
    src = NcSocialSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
