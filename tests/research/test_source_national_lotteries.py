"""Tests for the NL (alt) tender source plug-in."""
import pytest


def test_national_lotteries_source_initialization():
    from tender_getter.sources.research.national_lotteries import NationalLotteriesSource
    src = NationalLotteriesSource()
    assert src.source_id == "national_lotteries"
    assert isinstance(src.live, bool)


def test_national_lotteries_parse_mock_html():
    from tender_getter.sources.research.national_lotteries import NationalLotteriesSource, MOCK_HTML
    src = NationalLotteriesSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_national_lotteries_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.national_lotteries import NationalLotteriesSource
    src = NationalLotteriesSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
