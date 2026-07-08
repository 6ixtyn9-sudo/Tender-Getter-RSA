"""Tests for the Social Work Council tender source plug-in."""
import pytest


def test_social_work_council_source_initialization():
    from tender_getter.sources.research.social_work_council import SocialWorkCouncilSource
    src = SocialWorkCouncilSource()
    assert src.source_id == "social_work_council"
    assert src.live is False


def test_social_work_council_parse_mock_html():
    from tender_getter.sources.research.social_work_council import SocialWorkCouncilSource, MOCK_HTML
    src = SocialWorkCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_social_work_council_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.social_work_council import SocialWorkCouncilSource
    src = SocialWorkCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
