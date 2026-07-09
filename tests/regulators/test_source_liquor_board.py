"""Tests for the Liquor Board (collective) tender source plug-in."""
import pytest


def test_liquor_board_source_initialization():
    from tender_getter.sources.regulators.liquor_board import LiquorBoardSource
    src = LiquorBoardSource()
    assert src.source_id == "liquor_board"
    assert isinstance(src.live, bool)


def test_liquor_board_parse_mock_html():
    from tender_getter.sources.regulators.liquor_board import LiquorBoardSource, MOCK_HTML
    src = LiquorBoardSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_liquor_board_fetch_uses_fallback_on_empty():
    from tender_getter.sources.regulators.liquor_board import LiquorBoardSource
    src = LiquorBoardSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
