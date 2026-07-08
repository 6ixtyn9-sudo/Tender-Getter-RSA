"""Tests for the Financial Intelligence Centre (FIC) tender source plug-in."""
import pytest


def test_financial_intel_centre_source_initialization():
    from tender_getter.sources.schedule3a.financial_intel_centre import FinancialIntelCentreSource
    src = FinancialIntelCentreSource()
    assert src.source_id == "financial_intel_centre"
    assert src.live is True


def test_financial_intel_centre_parse_mock_html():
    from tender_getter.sources.schedule3a.financial_intel_centre import FinancialIntelCentreSource, MOCK_HTML
    src = FinancialIntelCentreSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_financial_intel_centre_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.financial_intel_centre import FinancialIntelCentreSource
    src = FinancialIntelCentreSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
