"""Tests for the North West Liquor Board tender source plug-in."""
import pytest


def test_nw_liquor_tenders_source_initialization():
    from tender_getter.sources.research_extra.nw_liquor_tenders import NwLiquorSource
    src = NwLiquorSource()
    assert src.source_id == "nw_liquor_tenders"
    assert src.live is False


def test_nw_liquor_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.nw_liquor_tenders import NwLiquorSource, MOCK_HTML
    src = NwLiquorSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nw_liquor_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.nw_liquor_tenders import NwLiquorSource
    src = NwLiquorSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
