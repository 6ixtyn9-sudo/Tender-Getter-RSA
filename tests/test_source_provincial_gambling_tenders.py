"""Tests for the Provincial Gambling tender source plug-in."""
import pytest


def test_provincial_gambling_tenders_source_initialization():
    from tender_getter.sources.research_extra.provincial_gambling_tenders import ProvincialGamblingSource
    src = ProvincialGamblingSource()
    assert src.source_id == "provincial_gambling_tenders"
    assert src.live is False


def test_provincial_gambling_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.provincial_gambling_tenders import ProvincialGamblingSource, MOCK_HTML
    src = ProvincialGamblingSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_provincial_gambling_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.provincial_gambling_tenders import ProvincialGamblingSource
    src = ProvincialGamblingSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
