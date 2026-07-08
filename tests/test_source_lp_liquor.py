"""Tests for the Limpopo Liquor Board tender source plug-in."""
import pytest


def test_lp_liquor_source_initialization():
    from tender_getter.sources.research.lp_liquor import LpLiquorSource
    src = LpLiquorSource()
    assert src.source_id == "lp_liquor"
    assert src.live is False


def test_lp_liquor_parse_mock_html():
    from tender_getter.sources.research.lp_liquor import LpLiquorSource, MOCK_HTML
    src = LpLiquorSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lp_liquor_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.lp_liquor import LpLiquorSource
    src = LpLiquorSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
