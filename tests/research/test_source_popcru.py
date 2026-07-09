"""Tests for the POPCRU tender source plug-in."""
import pytest


def test_popcru_source_initialization():
    from tender_getter.sources.research.popcru import PopcruSource
    src = PopcruSource()
    assert src.source_id == "popcru"
    assert isinstance(src.live, bool)


def test_popcru_parse_mock_html():
    from tender_getter.sources.research.popcru import PopcruSource, MOCK_HTML
    src = PopcruSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_popcru_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.popcru import PopcruSource
    src = PopcruSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
