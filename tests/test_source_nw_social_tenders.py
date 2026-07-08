"""Tests for the North West Social Development tender source plug-in."""
import pytest


def test_nw_social_tenders_source_initialization():
    from tender_getter.sources.research_extra.nw_social_tenders import NwSocialSource
    src = NwSocialSource()
    assert src.source_id == "nw_social_tenders"
    assert src.live is False


def test_nw_social_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.nw_social_tenders import NwSocialSource, MOCK_HTML
    src = NwSocialSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nw_social_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.nw_social_tenders import NwSocialSource
    src = NwSocialSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
