import pytest
from tender_getter.sources.provincial_depts.fs_police_roads import FSPoliceRoadsSource, MOCK_FS_POLICE_ROADS_HTML
def test_fs_police_roads_source_initialization():
    source = FSPoliceRoadsSource()
    assert source.source_id == "fs_police_roads_tenders"
    assert source.url.startswith("http")
def test_fs_police_roads_parse_mock_html():
    source = FSPoliceRoadsSource()
    tenders = source.parse_html(MOCK_FS_POLICE_ROADS_HTML)
    assert len(tenders) == 3
def test_fs_police_roads_fetch_uses_fallback_on_empty_or_error():
    source = FSPoliceRoadsSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
