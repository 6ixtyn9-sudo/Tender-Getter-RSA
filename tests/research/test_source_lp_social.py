"""Tests for the Limpopo Social Development tender source plug-in."""
import pytest


def test_lp_social_source_initialization():
    from tender_getter.sources.research.lp_social import LpSocialSource
    src = LpSocialSource()
    assert src.source_id == "lp_social"
    assert isinstance(src.live, bool)


def test_lp_social_parse_mock_html():
    from tender_getter.sources.research.lp_social import LpSocialSource, MOCK_HTML
    src = LpSocialSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lp_social_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.lp_social import LpSocialSource
    src = LpSocialSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
