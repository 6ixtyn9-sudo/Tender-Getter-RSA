"""Tests for the NGB (alt) tender source plug-in."""
import pytest


def test_national_gambling_board_tenders_source_initialization():
    from tender_getter.sources.research_extra.national_gambling_board_tenders import NationalGamblingBoardSource
    src = NationalGamblingBoardSource()
    assert src.source_id == "national_gambling_board_tenders"
    assert src.live is True


def test_national_gambling_board_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.national_gambling_board_tenders import NationalGamblingBoardSource, MOCK_HTML
    src = NationalGamblingBoardSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_national_gambling_board_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.national_gambling_board_tenders import NationalGamblingBoardSource
    src = NationalGamblingBoardSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
