"""Tests for the City of Cape Town Electricity Services tender source plug-in."""
import pytest


def test_coct_electricity_source_initialization():
    from tender_getter.sources.local_municipalities.coct_electricity import CoctElectricitySource
    src = CoctElectricitySource()
    assert src.source_id == "coct_electricity"
    assert src.live is True


def test_coct_electricity_parse_mock_html():
    from tender_getter.sources.local_municipalities.coct_electricity import CoctElectricitySource, MOCK_HTML
    src = CoctElectricitySource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_coct_electricity_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.coct_electricity import CoctElectricitySource
    src = CoctElectricitySource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
