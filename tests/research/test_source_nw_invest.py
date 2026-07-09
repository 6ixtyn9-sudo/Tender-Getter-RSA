"""Tests for the North West Investment tender source plug-in."""
import pytest


def test_nw_invest_source_initialization():
    from tender_getter.sources.research.nw_invest import NwInvestSource
    src = NwInvestSource()
    assert src.source_id == "nw_invest"
    assert isinstance(src.live, bool)


def test_nw_invest_parse_mock_html():
    from tender_getter.sources.research.nw_invest import NwInvestSource, MOCK_HTML
    src = NwInvestSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nw_invest_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nw_invest import NwInvestSource
    src = NwInvestSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
