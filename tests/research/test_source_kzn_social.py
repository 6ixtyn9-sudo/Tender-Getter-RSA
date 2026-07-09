"""Tests for the KZN Social Development tender source plug-in."""
import pytest


def test_kzn_social_source_initialization():
    from tender_getter.sources.research.kzn_social import KznSocialSource
    src = KznSocialSource()
    assert src.source_id == "kzn_social"
    assert src.live is False


def test_kzn_social_parse_mock_html():
    from tender_getter.sources.research.kzn_social import KznSocialSource, MOCK_HTML
    src = KznSocialSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kzn_social_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.kzn_social import KznSocialSource
    src = KznSocialSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
