"""Tests for the Eastern Cape Housing Board tender source plug-in."""
import pytest


def test_ec_housing_source_initialization():
    from tender_getter.sources.research.ec_housing import EcHousingSource
    src = EcHousingSource()
    assert src.source_id == "ec_housing"
    assert src.live is False


def test_ec_housing_parse_mock_html():
    from tender_getter.sources.research.ec_housing import EcHousingSource, MOCK_HTML
    src = EcHousingSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ec_housing_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.ec_housing import EcHousingSource
    src = EcHousingSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
