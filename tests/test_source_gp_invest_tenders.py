"""Tests for the Gauteng Investment Centre tender source plug-in."""
import pytest


def test_gp_invest_tenders_source_initialization():
    from tender_getter.sources.research_extra.gp_invest_tenders import GpInvestSource
    src = GpInvestSource()
    assert src.source_id == "gp_invest_tenders"
    assert src.live is False


def test_gp_invest_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.gp_invest_tenders import GpInvestSource, MOCK_HTML
    src = GpInvestSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gp_invest_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.gp_invest_tenders import GpInvestSource
    src = GpInvestSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
