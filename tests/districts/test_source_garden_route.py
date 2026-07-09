import pytest
from tender_getter.sources.districts.garden_route import GardenRouteSource, MOCK_GARDEN_ROUTE_HTML
def test_garden_route_source_initialization():
    source = GardenRouteSource()
    assert source.source_id == "garden_route"
    assert source.url.startswith("http")
def test_garden_route_parse_mock_html():
    source = GardenRouteSource()
    tenders = source.parse_html(MOCK_GARDEN_ROUTE_HTML)
    assert len(tenders) == 3
def test_garden_route_fetch_uses_fallback_on_empty_or_error():
    source = GardenRouteSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
