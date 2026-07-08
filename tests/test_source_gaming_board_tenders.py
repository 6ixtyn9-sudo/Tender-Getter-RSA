"""Tests for the Gaming Board tender source plug-in."""
import pytest


def test_gaming_board_tenders_source_initialization():
    from tender_getter.sources.research_extra.gaming_board_tenders import GamingBoardSource
    src = GamingBoardSource()
    assert src.source_id == "gaming_board_tenders"
    assert src.live is False


def test_gaming_board_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.gaming_board_tenders import GamingBoardSource, MOCK_HTML
    src = GamingBoardSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gaming_board_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.gaming_board_tenders import GamingBoardSource
    src = GamingBoardSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
