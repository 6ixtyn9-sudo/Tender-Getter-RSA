"""Tests for the SABC TV Licence tender source plug-in."""
import pytest


def test_sabc_tv_licence_source_initialization():
    from tender_getter.sources.research.sabc_tv_licence import SabcTvLicenceSource
    src = SabcTvLicenceSource()
    assert src.source_id == "sabc_tv_licence"
    assert src.live is False


def test_sabc_tv_licence_parse_mock_html():
    from tender_getter.sources.research.sabc_tv_licence import SabcTvLicenceSource, MOCK_HTML
    src = SabcTvLicenceSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sabc_tv_licence_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.sabc_tv_licence import SabcTvLicenceSource
    src = SabcTvLicenceSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
