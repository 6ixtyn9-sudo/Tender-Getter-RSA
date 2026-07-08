"""Tests for the Gauteng Liquor Board tender source plug-in."""
import pytest


def test_gp_liquor_source_initialization():
    from tender_getter.sources.research.gp_liquor import GpLiquorSource
    src = GpLiquorSource()
    assert src.source_id == "gp_liquor"
    assert src.live is False


def test_gp_liquor_parse_mock_html():
    from tender_getter.sources.research.gp_liquor import GpLiquorSource, MOCK_HTML
    src = GpLiquorSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gp_liquor_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.gp_liquor import GpLiquorSource
    src = GpLiquorSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
