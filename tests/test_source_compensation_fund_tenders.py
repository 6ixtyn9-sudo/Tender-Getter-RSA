"""Tests for the Compensation Fund tender source plug-in."""
import pytest


def test_compensation_fund_tenders_source_initialization():
    from tender_getter.sources.research_extra.compensation_fund_tenders import CompensationFundSource
    src = CompensationFundSource()
    assert src.source_id == "compensation_fund_tenders"
    assert src.live is True


def test_compensation_fund_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.compensation_fund_tenders import CompensationFundSource, MOCK_HTML
    src = CompensationFundSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_compensation_fund_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.compensation_fund_tenders import CompensationFundSource
    src = CompensationFundSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
