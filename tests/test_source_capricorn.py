import pytest
from tender_getter.sources.districts.capricorn import CapricornSource, MOCK_CAPRICORN_HTML
def test_capricorn_source_initialization():
    source = CapricornSource()
    assert source.source_id == "capricorn_tenders"
    assert source.url.startswith("http")
def test_capricorn_parse_mock_html():
    source = CapricornSource()
    tenders = source.parse_html(MOCK_CAPRICORN_HTML)
    assert len(tenders) == 3
def test_capricorn_fetch_uses_fallback_on_empty_or_error():
    source = CapricornSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
