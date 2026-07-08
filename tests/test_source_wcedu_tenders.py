"""Tests for the Western Cape Education Department (alt) tender source plug-in."""
import pytest


def test_wcedu_tenders_source_initialization():
    from tender_getter.sources.research_extra.wcedu_tenders import WceduSource
    src = WceduSource()
    assert src.source_id == "wcedu_tenders"
    assert src.live is True


def test_wcedu_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.wcedu_tenders import WceduSource, MOCK_HTML
    src = WceduSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wcedu_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.wcedu_tenders import WceduSource
    src = WceduSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
