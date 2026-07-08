"""Tests for the Trade and Investment KZN (TIK) tender source plug-in."""
import pytest


def test_kzn_invest_source_initialization():
    from tender_getter.sources.research.kzn_invest import KznInvestSource
    src = KznInvestSource()
    assert src.source_id == "kzn_invest"
    assert src.live is True


def test_kzn_invest_parse_mock_html():
    from tender_getter.sources.research.kzn_invest import KznInvestSource, MOCK_HTML
    src = KznInvestSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kzn_invest_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.kzn_invest import KznInvestSource
    src = KznInvestSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
