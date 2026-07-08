"""Tests for the Eastern Cape Social Development tender source plug-in."""
import pytest


def test_ec_social_source_initialization():
    from tender_getter.sources.research.ec_social import EcSocialSource
    src = EcSocialSource()
    assert src.source_id == "ec_social"
    assert src.live is False


def test_ec_social_parse_mock_html():
    from tender_getter.sources.research.ec_social import EcSocialSource, MOCK_HTML
    src = EcSocialSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ec_social_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.ec_social import EcSocialSource
    src = EcSocialSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
