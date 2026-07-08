"""Tests for the Eastern Cape Housing Board tender source plug-in."""
import pytest


def test_ec_housing_tenders_source_initialization():
    from tender_getter.sources.research_extra.ec_housing_tenders import EcHousingSource
    src = EcHousingSource()
    assert src.source_id == "ec_housing_tenders"
    assert src.live is False


def test_ec_housing_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.ec_housing_tenders import EcHousingSource, MOCK_HTML
    src = EcHousingSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ec_housing_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.ec_housing_tenders import EcHousingSource
    src = EcHousingSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
