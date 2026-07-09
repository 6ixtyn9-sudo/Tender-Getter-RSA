"""Tests for the Eastern Cape Investment Agency tender source plug-in."""
import pytest


def test_ec_invest_source_initialization():
    from tender_getter.sources.research.ec_invest import EcInvestSource
    src = EcInvestSource()
    assert src.source_id == "ec_invest"
    assert isinstance(src.live, bool)


def test_ec_invest_parse_mock_html():
    from tender_getter.sources.research.ec_invest import EcInvestSource, MOCK_HTML
    src = EcInvestSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ec_invest_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.ec_invest import EcInvestSource
    src = EcInvestSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
