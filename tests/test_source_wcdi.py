import pytest
from tender_getter.sources.provincial_depts.wcdi import WCDISource, MOCK_WCDI_HTML
def test_wcdi_source_initialization():
    source = WCDISource()
    assert source.source_id == "wcdi"
    assert source.url.startswith("http")
def test_wcdi_parse_mock_html():
    source = WCDISource()
    tenders = source.parse_html(MOCK_WCDI_HTML)
    assert len(tenders) == 3
def test_wcdi_fetch_uses_fallback_on_empty_or_error():
    source = WCDISource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
