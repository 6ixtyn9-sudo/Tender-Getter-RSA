"""Tests for the National Treasury tender source plug-in."""
import pytest


def test_national_treasury_tenders_source_initialization():
    from tender_getter.sources.research_extra.national_treasury_tenders import NationalTreasurySource
    src = NationalTreasurySource()
    assert src.source_id == "national_treasury_tenders"
    assert src.live is True


def test_national_treasury_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.national_treasury_tenders import NationalTreasurySource, MOCK_HTML
    src = NationalTreasurySource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_national_treasury_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.national_treasury_tenders import NationalTreasurySource
    src = NationalTreasurySource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
