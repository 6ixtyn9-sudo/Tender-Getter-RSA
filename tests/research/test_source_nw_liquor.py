"""Tests for the North West Liquor Board tender source plug-in."""
import pytest


def test_nw_liquor_source_initialization():
    from tender_getter.sources.research.nw_liquor import NwLiquorSource
    src = NwLiquorSource()
    assert src.source_id == "nw_liquor"
    assert isinstance(src.live, bool)


def test_nw_liquor_parse_mock_html():
    from tender_getter.sources.research.nw_liquor import NwLiquorSource, MOCK_HTML
    src = NwLiquorSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nw_liquor_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nw_liquor import NwLiquorSource
    src = NwLiquorSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
