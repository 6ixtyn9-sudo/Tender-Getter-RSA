"""Tests for the Garden Route (DM alt URL) tender source plug-in."""
import pytest


def test_garden_route_dm_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.garden_route_dm_alt_tenders import GardenRouteDmAltSource
    src = GardenRouteDmAltSource()
    assert src.source_id == "garden_route_dm_alt_tenders"
    assert src.live is False


def test_garden_route_dm_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.garden_route_dm_alt_tenders import GardenRouteDmAltSource, MOCK_HTML
    src = GardenRouteDmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_garden_route_dm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.garden_route_dm_alt_tenders import GardenRouteDmAltSource
    src = GardenRouteDmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
