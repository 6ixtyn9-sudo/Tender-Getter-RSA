"""Tests for the Ombudsman for Banking Services tender source plug-in."""
import pytest


def test_banking_ombud_tenders_source_initialization():
    from tender_getter.sources.schedule3a.banking_ombud_tenders import BankingOmbudSource
    src = BankingOmbudSource()
    assert src.source_id == "banking_ombud_tenders"
    assert src.live is True


def test_banking_ombud_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.banking_ombud_tenders import BankingOmbudSource, MOCK_HTML
    src = BankingOmbudSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_banking_ombud_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.banking_ombud_tenders import BankingOmbudSource
    src = BankingOmbudSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
