"""Tests for the Gauteng Social Development tender source plug-in."""
import pytest


def test_gp_social_source_initialization():
    from tender_getter.sources.research.gp_social import GpSocialSource
    src = GpSocialSource()
    assert src.source_id == "gp_social"
    assert src.live is False


def test_gp_social_parse_mock_html():
    from tender_getter.sources.research.gp_social import GpSocialSource, MOCK_HTML
    src = GpSocialSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gp_social_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.gp_social import GpSocialSource
    src = GpSocialSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
