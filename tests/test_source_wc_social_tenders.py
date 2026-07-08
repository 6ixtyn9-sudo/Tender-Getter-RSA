"""Tests for the Western Cape Social Development tender source plug-in."""
import pytest


def test_wc_social_tenders_source_initialization():
    from tender_getter.sources.research_extra.wc_social_tenders import WcSocialSource
    src = WcSocialSource()
    assert src.source_id == "wc_social_tenders"
    assert src.live is False


def test_wc_social_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.wc_social_tenders import WcSocialSource, MOCK_HTML
    src = WcSocialSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wc_social_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.wc_social_tenders import WcSocialSource
    src = WcSocialSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
