"""Tests for the Mpumalanga Liquor Board tender source plug-in."""
import pytest


def test_mp_liquor_tenders_source_initialization():
    from tender_getter.sources.research_extra.mp_liquor_tenders import MpLiquorSource
    src = MpLiquorSource()
    assert src.source_id == "mp_liquor_tenders"
    assert src.live is False


def test_mp_liquor_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.mp_liquor_tenders import MpLiquorSource, MOCK_HTML
    src = MpLiquorSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mp_liquor_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.mp_liquor_tenders import MpLiquorSource
    src = MpLiquorSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
