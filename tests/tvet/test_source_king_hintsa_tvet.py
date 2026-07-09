"""Tests for the King Hintsa TVET College tender source plug-in."""
import pytest


def test_king_hintsa_tvet_source_initialization():
    from tender_getter.sources.tvet.king_hintsa_tvet import KingHintsaTvetSource
    src = KingHintsaTvetSource()
    assert src.source_id == "king_hintsa_tvet"
    assert isinstance(src.live, bool)


def test_king_hintsa_tvet_parse_mock_html():
    from tender_getter.sources.tvet.king_hintsa_tvet import KingHintsaTvetSource, MOCK_HTML
    src = KingHintsaTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_king_hintsa_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.king_hintsa_tvet import KingHintsaTvetSource
    src = KingHintsaTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
