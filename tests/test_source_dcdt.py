import pytest
from tender_getter.sources.national_depts.dcdt import DCDTSource, MOCK_DCDT_HTML
def test_dcdt_source_initialization():
    source = DCDTSource()
    assert source.source_id == "dcdt_tenders"
    assert source.url.startswith("http")
def test_dcdt_parse_mock_html():
    source = DCDTSource()
    tenders = source.parse_html(MOCK_DCDT_HTML)
    assert len(tenders) == 3
def test_dcdt_fetch_uses_fallback_on_empty_or_error():
    source = DCDTSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
