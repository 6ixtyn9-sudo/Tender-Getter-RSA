"""Tests for the Mpumalanga Social Development tender source plug-in."""
import pytest


def test_mp_social_source_initialization():
    from tender_getter.sources.research.mp_social import MpSocialSource
    src = MpSocialSource()
    assert src.source_id == "mp_social"
    assert src.live is False


def test_mp_social_parse_mock_html():
    from tender_getter.sources.research.mp_social import MpSocialSource, MOCK_HTML
    src = MpSocialSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mp_social_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.mp_social import MpSocialSource
    src = MpSocialSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
