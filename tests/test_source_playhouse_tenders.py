"""Tests for the Playhouse Company tender source plug-in."""
import pytest


def test_playhouse_tenders_source_initialization():
    from tender_getter.sources.research_extra.playhouse_tenders import PlayhouseSource
    src = PlayhouseSource()
    assert src.source_id == "playhouse_tenders"
    assert src.live is False


def test_playhouse_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.playhouse_tenders import PlayhouseSource, MOCK_HTML
    src = PlayhouseSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_playhouse_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.playhouse_tenders import PlayhouseSource
    src = PlayhouseSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
