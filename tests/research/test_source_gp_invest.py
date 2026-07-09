"""Tests for the Gauteng Investment Centre tender source plug-in."""
import pytest


def test_gp_invest_source_initialization():
    from tender_getter.sources.research.gp_invest import GpInvestSource
    src = GpInvestSource()
    assert src.source_id == "gp_invest"
    assert isinstance(src.live, bool)


def test_gp_invest_parse_mock_html():
    from tender_getter.sources.research.gp_invest import GpInvestSource, MOCK_HTML
    src = GpInvestSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gp_invest_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.gp_invest import GpInvestSource
    src = GpInvestSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
