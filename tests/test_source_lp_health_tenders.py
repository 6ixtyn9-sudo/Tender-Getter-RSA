"""Tests for the Limpopo Health tender source plug-in."""
import pytest


def test_lp_health_tenders_source_initialization():
    from tender_getter.sources.research_extra.lp_health_tenders import LpHealthSource
    src = LpHealthSource()
    assert src.source_id == "lp_health_tenders"
    assert src.live is True


def test_lp_health_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.lp_health_tenders import LpHealthSource, MOCK_HTML
    src = LpHealthSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lp_health_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.lp_health_tenders import LpHealthSource
    src = LpHealthSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
