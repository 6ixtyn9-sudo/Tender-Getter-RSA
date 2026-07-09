"""Tests for the Western Cape Education Department (alt) tender source plug-in."""
import pytest


def test_wcedu_source_initialization():
    from tender_getter.sources.research.wcedu import WceduSource
    src = WceduSource()
    assert src.source_id == "wcedu"
    assert src.live is True


def test_wcedu_parse_mock_html():
    from tender_getter.sources.research.wcedu import WceduSource, MOCK_HTML
    src = WceduSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wcedu_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.wcedu import WceduSource
    src = WceduSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
