"""Tests for the Northern Cape Social Development tender source plug-in."""
import pytest


def test_nc_social_tenders_source_initialization():
    from tender_getter.sources.research_extra.nc_social_tenders import NcSocialSource
    src = NcSocialSource()
    assert src.source_id == "nc_social_tenders"
    assert src.live is False


def test_nc_social_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.nc_social_tenders import NcSocialSource, MOCK_HTML
    src = NcSocialSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nc_social_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.nc_social_tenders import NcSocialSource
    src = NcSocialSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
