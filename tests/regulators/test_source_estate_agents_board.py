"""Tests for the EAAB tender source plug-in."""
import pytest


def test_estate_agents_board_source_initialization():
    from tender_getter.sources.regulators.estate_agents_board import EstateAgentsBoardSource
    src = EstateAgentsBoardSource()
    assert src.source_id == "estate_agents_board"
    assert isinstance(src.live, bool)


def test_estate_agents_board_parse_mock_html():
    from tender_getter.sources.regulators.estate_agents_board import EstateAgentsBoardSource, MOCK_HTML
    src = EstateAgentsBoardSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_estate_agents_board_fetch_uses_fallback_on_empty():
    from tender_getter.sources.regulators.estate_agents_board import EstateAgentsBoardSource
    src = EstateAgentsBoardSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
