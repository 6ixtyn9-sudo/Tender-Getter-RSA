import pytest
from tender_getter.sources.national_depts.dffe import DFFESource, MOCK_DFFE_HTML
def test_dffe_source_initialization():
    source = DFFESource()
    assert source.source_id == "dffe_tenders"
    assert source.url.startswith("http")
def test_dffe_parse_mock_html():
    source = DFFESource()
    tenders = source.parse_html(MOCK_DFFE_HTML)
    assert len(tenders) == 3
def test_dffe_fetch_uses_fallback_on_empty_or_error():
    source = DFFESource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
