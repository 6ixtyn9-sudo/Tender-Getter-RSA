"""Tests for the Playhouse Company tender source plug-in."""
import pytest


def test_playhouse_source_initialization():
    from tender_getter.sources.research.playhouse import PlayhouseSource
    src = PlayhouseSource()
    assert src.source_id == "playhouse"
    assert isinstance(src.live, bool)


def test_playhouse_parse_mock_html():
    from tender_getter.sources.research.playhouse import PlayhouseSource, MOCK_HTML
    src = PlayhouseSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_playhouse_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.playhouse import PlayhouseSource
    src = PlayhouseSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
