"""Tests for the iLembe District Municipality tender source plug-in."""
import pytest


def test_ilembe_tenders_source_initialization():
    from tender_getter.sources.research_extra.ilembe_tenders import IlembeSource
    src = IlembeSource()
    assert src.source_id == "ilembe_tenders"
    assert src.live is True


def test_ilembe_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.ilembe_tenders import IlembeSource, MOCK_HTML
    src = IlembeSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ilembe_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.ilembe_tenders import IlembeSource
    src = IlembeSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
