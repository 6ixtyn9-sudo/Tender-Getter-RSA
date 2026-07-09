"""Tests for the North West Social Development tender source plug-in."""
import pytest


def test_nw_social_source_initialization():
    from tender_getter.sources.research.nw_social import NwSocialSource
    src = NwSocialSource()
    assert src.source_id == "nw_social"
    assert isinstance(src.live, bool)


def test_nw_social_parse_mock_html():
    from tender_getter.sources.research.nw_social import NwSocialSource, MOCK_HTML
    src = NwSocialSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nw_social_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nw_social import NwSocialSource
    src = NwSocialSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
