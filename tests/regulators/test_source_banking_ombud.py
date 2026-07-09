"""Tests for the Ombudsman for Banking Services tender source plug-in."""
import pytest


def test_banking_ombud_source_initialization():
    from tender_getter.sources.regulators.banking_ombud import BankingOmbudSource
    src = BankingOmbudSource()
    assert src.source_id == "banking_ombud"
    assert isinstance(src.live, bool)


def test_banking_ombud_parse_mock_html():
    from tender_getter.sources.regulators.banking_ombud import BankingOmbudSource, MOCK_HTML
    src = BankingOmbudSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_banking_ombud_fetch_uses_fallback_on_empty():
    from tender_getter.sources.regulators.banking_ombud import BankingOmbudSource
    src = BankingOmbudSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
