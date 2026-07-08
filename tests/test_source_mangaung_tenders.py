"""Tests for the Mangaung Metropolitan Municipality tender source plug-in."""
import pytest


def test_mangaung_tenders_source_initialization():
    from tender_getter.sources.research_extra.mangaung_tenders import MangaungSource
    src = MangaungSource()
    assert src.source_id == "mangaung_tenders"
    assert src.live is True


def test_mangaung_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.mangaung_tenders import MangaungSource, MOCK_HTML
    src = MangaungSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mangaung_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.mangaung_tenders import MangaungSource
    src = MangaungSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
