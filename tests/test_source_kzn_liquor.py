"""Tests for the KZN Liquor Authority tender source plug-in."""
import pytest


def test_kzn_liquor_source_initialization():
    from tender_getter.sources.research.kzn_liquor import KznLiquorSource
    src = KznLiquorSource()
    assert src.source_id == "kzn_liquor"
    assert src.live is False


def test_kzn_liquor_parse_mock_html():
    from tender_getter.sources.research.kzn_liquor import KznLiquorSource, MOCK_HTML
    src = KznLiquorSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kzn_liquor_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.kzn_liquor import KznLiquorSource
    src = KznLiquorSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
