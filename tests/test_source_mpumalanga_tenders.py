"""Tests for the Mpumalanga Provincial Treasury tender source plug-in."""
import pytest


def test_mpumalanga_tenders_source_initialization():
    from tender_getter.sources.research_extra.mpumalanga_tenders import MpumalangaSource
    src = MpumalangaSource()
    assert src.source_id == "mpumalanga_tenders"
    assert src.live is True


def test_mpumalanga_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.mpumalanga_tenders import MpumalangaSource, MOCK_HTML
    src = MpumalangaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mpumalanga_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.mpumalanga_tenders import MpumalangaSource
    src = MpumalangaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
