"""Tests for the NGB (alt) tender source plug-in."""
import pytest


def test_national_gambling_board_source_initialization():
    from tender_getter.sources.regulators.national_gambling_board import NationalGamblingBoardSource
    src = NationalGamblingBoardSource()
    assert src.source_id == "national_gambling_board"
    assert isinstance(src.live, bool)


def test_national_gambling_board_parse_mock_html():
    from tender_getter.sources.regulators.national_gambling_board import NationalGamblingBoardSource, MOCK_HTML
    src = NationalGamblingBoardSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_national_gambling_board_fetch_uses_fallback_on_empty():
    from tender_getter.sources.regulators.national_gambling_board import NationalGamblingBoardSource
    src = NationalGamblingBoardSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
