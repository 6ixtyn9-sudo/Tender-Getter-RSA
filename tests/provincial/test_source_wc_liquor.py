"""Tests for the Western Cape Liquor Authority tender source plug-in."""
import pytest


def test_wc_liquor_source_initialization():
    from tender_getter.sources.provincial.wc_liquor import WcLiquorSource
    src = WcLiquorSource()
    assert src.source_id == "wc_liquor"
    assert src.live is False


def test_wc_liquor_parse_mock_html():
    from tender_getter.sources.provincial.wc_liquor import WcLiquorSource, MOCK_HTML
    src = WcLiquorSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wc_liquor_fetch_uses_fallback_on_empty():
    from tender_getter.sources.provincial.wc_liquor import WcLiquorSource
    src = WcLiquorSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
