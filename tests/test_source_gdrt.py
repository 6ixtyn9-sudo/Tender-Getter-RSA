import pytest
from tender_getter.sources.provincial_depts.gdrt import GDRTSource, MOCK_GDRT_HTML
def test_gdrt_source_initialization():
    source = GDRTSource()
    assert source.source_id == "gdrt"
    assert source.url.startswith("http")
def test_gdrt_parse_mock_html():
    source = GDRTSource()
    tenders = source.parse_html(MOCK_GDRT_HTML)
    assert len(tenders) == 3
def test_gdrt_fetch_uses_fallback_on_empty_or_error():
    source = GDRTSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
