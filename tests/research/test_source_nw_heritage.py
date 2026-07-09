"""Tests for the North West Heritage Foundation tender source plug-in."""
import pytest


def test_nw_heritage_source_initialization():
    from tender_getter.sources.research.nw_heritage import NwHeritageSource
    src = NwHeritageSource()
    assert src.source_id == "nw_heritage"
    assert isinstance(src.live, bool)


def test_nw_heritage_parse_mock_html():
    from tender_getter.sources.research.nw_heritage import NwHeritageSource, MOCK_HTML
    src = NwHeritageSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nw_heritage_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nw_heritage import NwHeritageSource
    src = NwHeritageSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
