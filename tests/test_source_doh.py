import pytest
from tender_getter.sources.national_depts.doh import DoHSource, MOCK_DOH_HTML
def test_doh_source_initialization():
    source = DoHSource()
    assert source.source_id == "doh_tenders"
    assert source.url.startswith("http")
def test_doh_parse_mock_html():
    source = DoHSource()
    tenders = source.parse_html(MOCK_DOH_HTML)
    assert len(tenders) == 3
def test_doh_fetch_uses_fallback_on_empty_or_error():
    source = DoHSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
