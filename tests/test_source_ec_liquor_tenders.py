"""Tests for the Eastern Cape Liquor Board tender source plug-in."""
import pytest


def test_ec_liquor_tenders_source_initialization():
    from tender_getter.sources.research_extra.ec_liquor_tenders import EcLiquorSource
    src = EcLiquorSource()
    assert src.source_id == "ec_liquor_tenders"
    assert src.live is False


def test_ec_liquor_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.ec_liquor_tenders import EcLiquorSource, MOCK_HTML
    src = EcLiquorSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ec_liquor_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.ec_liquor_tenders import EcLiquorSource
    src = EcLiquorSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
