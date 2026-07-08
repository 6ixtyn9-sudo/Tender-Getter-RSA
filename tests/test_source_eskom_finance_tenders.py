"""Tests for the Eskom Finance Company tender source plug-in."""
import pytest


def test_eskom_finance_tenders_source_initialization():
    from tender_getter.sources.soes_extra.eskom_finance_tenders import EskomFinanceSource
    src = EskomFinanceSource()
    assert src.source_id == "eskom_finance_tenders"
    assert src.live is False


def test_eskom_finance_tenders_parse_mock_html():
    from tender_getter.sources.soes_extra.eskom_finance_tenders import EskomFinanceSource, MOCK_HTML
    src = EskomFinanceSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_eskom_finance_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes_extra.eskom_finance_tenders import EskomFinanceSource
    src = EskomFinanceSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
