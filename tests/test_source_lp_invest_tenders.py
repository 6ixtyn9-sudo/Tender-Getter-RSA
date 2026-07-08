"""Tests for the Limpopo Investment tender source plug-in."""
import pytest


def test_lp_invest_tenders_source_initialization():
    from tender_getter.sources.research_extra.lp_invest_tenders import LpInvestSource
    src = LpInvestSource()
    assert src.source_id == "lp_invest_tenders"
    assert src.live is False


def test_lp_invest_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.lp_invest_tenders import LpInvestSource, MOCK_HTML
    src = LpInvestSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lp_invest_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.lp_invest_tenders import LpInvestSource
    src = LpInvestSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
