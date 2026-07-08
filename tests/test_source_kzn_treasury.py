"""Tests for the KwaZulu-Natal Treasury tender source plug-in."""
import pytest


def test_kzn_treasury_source_initialization():
    from tender_getter.sources.research_extra.kzn_treasury import KznTreasurySource
    src = KznTreasurySource()
    assert src.source_id == "kzn_treasury"
    assert src.live is True


def test_kzn_treasury_parse_mock_html():
    from tender_getter.sources.research_extra.kzn_treasury import KznTreasurySource, MOCK_HTML
    src = KznTreasurySource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kzn_treasury_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.kzn_treasury import KznTreasurySource
    src = KznTreasurySource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
