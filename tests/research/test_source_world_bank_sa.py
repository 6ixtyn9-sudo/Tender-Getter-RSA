"""Tests for the World Bank SA tender source plug-in."""
import pytest


def test_world_bank_sa_source_initialization():
    from tender_getter.sources.research.world_bank_sa import WorldBankSaSource
    src = WorldBankSaSource()
    assert src.source_id == "world_bank_sa"
    assert isinstance(src.live, bool)


def test_world_bank_sa_parse_mock_html():
    from tender_getter.sources.research.world_bank_sa import WorldBankSaSource, MOCK_HTML
    src = WorldBankSaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_world_bank_sa_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.world_bank_sa import WorldBankSaSource
    src = WorldBankSaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
