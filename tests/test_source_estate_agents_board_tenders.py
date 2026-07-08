"""Tests for the EAAB tender source plug-in."""
import pytest


def test_estate_agents_board_tenders_source_initialization():
    from tender_getter.sources.research_extra.estate_agents_board_tenders import EstateAgentsBoardSource
    src = EstateAgentsBoardSource()
    assert src.source_id == "estate_agents_board_tenders"
    assert src.live is True


def test_estate_agents_board_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.estate_agents_board_tenders import EstateAgentsBoardSource, MOCK_HTML
    src = EstateAgentsBoardSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_estate_agents_board_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.estate_agents_board_tenders import EstateAgentsBoardSource
    src = EstateAgentsBoardSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
