"""Tests for the City of Tshwane Energy and Electricity Division tender source plug-in."""
import pytest


def test_tshwane_energy_source_initialization():
    from tender_getter.sources.research.tshwane_energy import TshwaneEnergySource
    src = TshwaneEnergySource()
    assert src.source_id == "tshwane_energy"
    assert src.live is True


def test_tshwane_energy_parse_mock_html():
    from tender_getter.sources.research.tshwane_energy import TshwaneEnergySource, MOCK_HTML
    src = TshwaneEnergySource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_tshwane_energy_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.tshwane_energy import TshwaneEnergySource
    src = TshwaneEnergySource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
