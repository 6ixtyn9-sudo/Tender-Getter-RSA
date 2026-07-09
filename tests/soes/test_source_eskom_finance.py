"""Tests for the Eskom Finance Company tender source plug-in."""
import pytest


def test_eskom_finance_source_initialization():
    from tender_getter.sources.soes.eskom_finance import EskomFinanceSource
    src = EskomFinanceSource()
    assert src.source_id == "eskom_finance"
    assert isinstance(src.live, bool)


def test_eskom_finance_parse_mock_html():
    from tender_getter.sources.soes.eskom_finance import EskomFinanceSource, MOCK_HTML
    src = EskomFinanceSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_eskom_finance_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.eskom_finance import EskomFinanceSource
    src = EskomFinanceSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
