"""Tests for the Banking Association tender source plug-in."""
import pytest


def test_banking_association_tenders_source_initialization():
    from tender_getter.sources.research_extra.banking_association_tenders import BankingAssociationSource
    src = BankingAssociationSource()
    assert src.source_id == "banking_association_tenders"
    assert src.live is False


def test_banking_association_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.banking_association_tenders import BankingAssociationSource, MOCK_HTML
    src = BankingAssociationSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_banking_association_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.banking_association_tenders import BankingAssociationSource
    src = BankingAssociationSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
