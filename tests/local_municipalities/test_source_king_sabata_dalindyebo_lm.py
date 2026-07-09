"""Tests for the King Sabata Dalindyebo Local Municipality tender source plug-in."""
import pytest


def test_king_sabata_dalindyebo_lm_source_initialization():
    from tender_getter.sources.local_municipalities.king_sabata_dalindyebo_lm import KingSabataDalindyeboLmSource
    src = KingSabataDalindyeboLmSource()
    assert src.source_id == "king_sabata_dalindyebo_lm"
    assert src.live is True


def test_king_sabata_dalindyebo_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.king_sabata_dalindyebo_lm import KingSabataDalindyeboLmSource, MOCK_HTML
    src = KingSabataDalindyeboLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_king_sabata_dalindyebo_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.king_sabata_dalindyebo_lm import KingSabataDalindyeboLmSource
    src = KingSabataDalindyeboLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
