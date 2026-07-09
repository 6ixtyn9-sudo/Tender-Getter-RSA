import pytest
from tender_getter.sources.national_depts.dws import DWSSource, MOCK_DWS_HTML
def test_dws_source_initialization():
    source = DWSSource()
    assert source.source_id == "dws"
    assert source.url.startswith("http")
def test_dws_parse_mock_html():
    source = DWSSource()
    tenders = source.parse_html(MOCK_DWS_HTML)
    assert len(tenders) == 3
def test_dws_fetch_uses_fallback_on_empty_or_error():
    source = DWSSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
