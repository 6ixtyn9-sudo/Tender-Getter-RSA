"""Tests for the NL (alt) tender source plug-in."""
import pytest


def test_national_lotteries_tenders_source_initialization():
    from tender_getter.sources.research_extra.national_lotteries_tenders import NationalLotteriesSource
    src = NationalLotteriesSource()
    assert src.source_id == "national_lotteries_tenders"
    assert src.live is True


def test_national_lotteries_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.national_lotteries_tenders import NationalLotteriesSource, MOCK_HTML
    src = NationalLotteriesSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_national_lotteries_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.national_lotteries_tenders import NationalLotteriesSource
    src = NationalLotteriesSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
