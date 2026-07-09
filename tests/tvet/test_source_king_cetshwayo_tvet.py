"""Tests for the King Cetshwayo TVET College tender source plug-in."""
import pytest


def test_king_cetshwayo_tvet_source_initialization():
    from tender_getter.sources.tvet.king_cetshwayo_tvet import KingCetshwayoTvetSource
    src = KingCetshwayoTvetSource()
    assert src.source_id == "king_cetshwayo_tvet"
    assert isinstance(src.live, bool)


def test_king_cetshwayo_tvet_parse_mock_html():
    from tender_getter.sources.tvet.king_cetshwayo_tvet import KingCetshwayoTvetSource, MOCK_HTML
    src = KingCetshwayoTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_king_cetshwayo_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.king_cetshwayo_tvet import KingCetshwayoTvetSource
    src = KingCetshwayoTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
