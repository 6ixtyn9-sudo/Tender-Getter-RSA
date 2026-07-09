"""Tests for the Limpopo Agriculture tender source plug-in."""
import pytest


def test_lp_agriculture_source_initialization():
    from tender_getter.sources.research.lp_agriculture import LpAgricultureSource
    src = LpAgricultureSource()
    assert src.source_id == "lp_agriculture"
    assert src.live is False


def test_lp_agriculture_parse_mock_html():
    from tender_getter.sources.research.lp_agriculture import LpAgricultureSource, MOCK_HTML
    src = LpAgricultureSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lp_agriculture_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.lp_agriculture import LpAgricultureSource
    src = LpAgricultureSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
