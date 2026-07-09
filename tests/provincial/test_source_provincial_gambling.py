"""Tests for the Provincial Gambling tender source plug-in."""
import pytest


def test_provincial_gambling_source_initialization():
    from tender_getter.sources.provincial.provincial_gambling import ProvincialGamblingSource
    src = ProvincialGamblingSource()
    assert src.source_id == "provincial_gambling"
    assert isinstance(src.live, bool)


def test_provincial_gambling_parse_mock_html():
    from tender_getter.sources.provincial.provincial_gambling import ProvincialGamblingSource, MOCK_HTML
    src = ProvincialGamblingSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_provincial_gambling_fetch_uses_fallback_on_empty():
    from tender_getter.sources.provincial.provincial_gambling import ProvincialGamblingSource
    src = ProvincialGamblingSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
