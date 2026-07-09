"""Tests for the ACSA (alt) tender source plug-in."""
import pytest


def test_airports_company_source_initialization():
    from tender_getter.sources.research.airports_company import AirportsCompanySource
    src = AirportsCompanySource()
    assert src.source_id == "airports_company"
    assert src.live is True


def test_airports_company_parse_mock_html():
    from tender_getter.sources.research.airports_company import AirportsCompanySource, MOCK_HTML
    src = AirportsCompanySource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_airports_company_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.airports_company import AirportsCompanySource
    src = AirportsCompanySource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
