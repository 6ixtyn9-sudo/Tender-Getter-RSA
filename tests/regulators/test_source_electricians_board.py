"""Tests for the Electricians Board tender source plug-in."""
import pytest


def test_electricians_board_source_initialization():
    from tender_getter.sources.regulators.electricians_board import ElectriciansBoardSource
    src = ElectriciansBoardSource()
    assert src.source_id == "electricians_board"
    assert src.live is False


def test_electricians_board_parse_mock_html():
    from tender_getter.sources.regulators.electricians_board import ElectriciansBoardSource, MOCK_HTML
    src = ElectriciansBoardSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_electricians_board_fetch_uses_fallback_on_empty():
    from tender_getter.sources.regulators.electricians_board import ElectriciansBoardSource
    src = ElectriciansBoardSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
