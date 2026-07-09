import pytest
from tender_getter.sources.research.nhls import NHLSSource, MOCK_NHLS_HTML
def test_nhls_source_initialization():
    source = NHLSSource()
    assert source.source_id == "nhls"
    assert source.url.startswith("http")
def test_nhls_parse_mock_html():
    source = NHLSSource()
    tenders = source.parse_html(MOCK_NHLS_HTML)
    assert len(tenders) == 3
def test_nhls_fetch_uses_fallback_on_empty_or_error():
    source = NHLSSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
