"""Tests for the Electricians Board tender source plug-in."""
import pytest


def test_electricians_board_tenders_source_initialization():
    from tender_getter.sources.research_extra.electricians_board_tenders import ElectriciansBoardSource
    src = ElectriciansBoardSource()
    assert src.source_id == "electricians_board_tenders"
    assert src.live is False


def test_electricians_board_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.electricians_board_tenders import ElectriciansBoardSource, MOCK_HTML
    src = ElectriciansBoardSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_electricians_board_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.electricians_board_tenders import ElectriciansBoardSource
    src = ElectriciansBoardSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
