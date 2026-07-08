import pytest
from tender_getter.sources.national_depts.dsi import DSISource, MOCK_DSI_HTML
def test_dsi_source_initialization():
    source = DSISource()
    assert source.source_id == "dsi_tenders"
    assert source.url.startswith("http")
def test_dsi_parse_mock_html():
    source = DSISource()
    tenders = source.parse_html(MOCK_DSI_HTML)
    assert len(tenders) == 3
def test_dsi_fetch_uses_fallback_on_empty_or_error():
    source = DSISource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
