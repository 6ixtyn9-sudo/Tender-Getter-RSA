"""Tests for the Western Cape Housing tender source plug-in."""
import pytest


def test_wc_housing_tenders_source_initialization():
    from tender_getter.sources.research_extra.wc_housing_tenders import WcHousingSource
    src = WcHousingSource()
    assert src.source_id == "wc_housing_tenders"
    assert src.live is False


def test_wc_housing_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.wc_housing_tenders import WcHousingSource, MOCK_HTML
    src = WcHousingSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wc_housing_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.wc_housing_tenders import WcHousingSource
    src = WcHousingSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
