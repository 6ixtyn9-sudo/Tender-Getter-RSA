"""Tests for the Banking Sector Education and Training Authority (BANKSETA) tender source plug-in."""
import pytest


def test_bankseta_source_initialization():
    from tender_getter.sources.setas.bankseta import BanksetaSource
    src = BanksetaSource()
    assert src.source_id == "bankseta"
    assert isinstance(src.live, bool)


def test_bankseta_parse_mock_html():
    from tender_getter.sources.setas.bankseta import BanksetaSource, MOCK_HTML
    src = BanksetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_bankseta_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.bankseta import BanksetaSource
    src = BanksetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
