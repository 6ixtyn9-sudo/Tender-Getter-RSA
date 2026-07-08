"""Tests for the Compensation Fund (alt) tender source plug-in."""
import pytest


def test_compensation_fund_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.compensation_fund_alt_tenders import CompensationFundAltSource
    src = CompensationFundAltSource()
    assert src.source_id == "compensation_fund_alt_tenders"
    assert src.live is True


def test_compensation_fund_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.compensation_fund_alt_tenders import CompensationFundAltSource, MOCK_HTML
    src = CompensationFundAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_compensation_fund_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.compensation_fund_alt_tenders import CompensationFundAltSource
    src = CompensationFundAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
