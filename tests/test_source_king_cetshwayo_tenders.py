"""Tests for the King Cetshwayo District Municipality tender source plug-in."""
import pytest


def test_king_cetshwayo_tenders_source_initialization():
    from tender_getter.sources.research_extra.king_cetshwayo_tenders import KingCetshwayoSource
    src = KingCetshwayoSource()
    assert src.source_id == "king_cetshwayo_tenders"
    assert src.live is True


def test_king_cetshwayo_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.king_cetshwayo_tenders import KingCetshwayoSource, MOCK_HTML
    src = KingCetshwayoSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_king_cetshwayo_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.king_cetshwayo_tenders import KingCetshwayoSource
    src = KingCetshwayoSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
