"""Tests for the Garden Route District Municipality tender source plug-in."""
import pytest


def test_garden_route_tenders_source_initialization():
    from tender_getter.sources.research_extra.garden_route_tenders import GardenRouteSource
    src = GardenRouteSource()
    assert src.source_id == "garden_route_tenders"
    assert src.live is True


def test_garden_route_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.garden_route_tenders import GardenRouteSource, MOCK_HTML
    src = GardenRouteSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_garden_route_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.garden_route_tenders import GardenRouteSource
    src = GardenRouteSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
