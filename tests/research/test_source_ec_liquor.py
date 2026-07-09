"""Tests for the Eastern Cape Liquor Board tender source plug-in."""
import pytest


def test_ec_liquor_source_initialization():
    from tender_getter.sources.research.ec_liquor import EcLiquorSource
    src = EcLiquorSource()
    assert src.source_id == "ec_liquor"
    assert isinstance(src.live, bool)


def test_ec_liquor_parse_mock_html():
    from tender_getter.sources.research.ec_liquor import EcLiquorSource, MOCK_HTML
    src = EcLiquorSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ec_liquor_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.ec_liquor import EcLiquorSource
    src = EcLiquorSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
