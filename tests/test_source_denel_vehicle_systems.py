"""Tests for the Denel Vehicle Systems tender source plug-in."""
import pytest


def test_denel_vehicle_systems_source_initialization():
    from tender_getter.sources.soes.denel_vehicle_systems import DenelVehicleSystemsSource
    src = DenelVehicleSystemsSource()
    assert src.source_id == "denel_vehicle_systems"
    assert src.live is True


def test_denel_vehicle_systems_parse_mock_html():
    from tender_getter.sources.soes.denel_vehicle_systems import DenelVehicleSystemsSource, MOCK_HTML
    src = DenelVehicleSystemsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_denel_vehicle_systems_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.denel_vehicle_systems import DenelVehicleSystemsSource
    src = DenelVehicleSystemsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
