"""Tests for the Plumbers Board tender source plug-in."""
import pytest


def test_plumbers_board_tenders_source_initialization():
    from tender_getter.sources.research_extra.plumbers_board_tenders import PlumbersBoardSource
    src = PlumbersBoardSource()
    assert src.source_id == "plumbers_board_tenders"
    assert src.live is False


def test_plumbers_board_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.plumbers_board_tenders import PlumbersBoardSource, MOCK_HTML
    src = PlumbersBoardSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_plumbers_board_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.plumbers_board_tenders import PlumbersBoardSource
    src = PlumbersBoardSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
