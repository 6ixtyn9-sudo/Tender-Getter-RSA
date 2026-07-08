"""Tests for the Limpopo Agriculture tender source plug-in."""
import pytest


def test_lp_agriculture_tenders_source_initialization():
    from tender_getter.sources.research_extra.lp_agriculture_tenders import LpAgricultureSource
    src = LpAgricultureSource()
    assert src.source_id == "lp_agriculture_tenders"
    assert src.live is False


def test_lp_agriculture_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.lp_agriculture_tenders import LpAgricultureSource, MOCK_HTML
    src = LpAgricultureSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lp_agriculture_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.lp_agriculture_tenders import LpAgricultureSource
    src = LpAgricultureSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
