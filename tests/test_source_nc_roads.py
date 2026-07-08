import pytest
from tender_getter.sources.provincial_depts.nc_roads import NCRoadsSource, MOCK_NC_ROADS_HTML
def test_nc_roads_source_initialization():
    source = NCRoadsSource()
    assert source.source_id == "nc_roads_tenders"
    assert source.url.startswith("http")
def test_nc_roads_parse_mock_html():
    source = NCRoadsSource()
    tenders = source.parse_html(MOCK_NC_ROADS_HTML)
    assert len(tenders) == 3
def test_nc_roads_fetch_uses_fallback_on_empty_or_error():
    source = NCRoadsSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
