import pytest
from tender_getter.sources.districts.west_rand import WestRandSource, MOCK_WEST_RAND_HTML
def test_west_rand_source_initialization():
    source = WestRandSource()
    assert source.source_id == "west_rand_tenders"
    assert source.url.startswith("http")
def test_west_rand_parse_mock_html():
    source = WestRandSource()
    tenders = source.parse_html(MOCK_WEST_RAND_HTML)
    assert len(tenders) == 3
def test_west_rand_fetch_uses_fallback_on_empty_or_error():
    source = WestRandSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
