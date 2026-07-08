import pytest
from tender_getter.sources.national_depts.dsac import DSACSource, MOCK_DSAC_HTML
def test_dsac_source_initialization():
    source = DSACSource()
    assert source.source_id == "dsac_tenders"
    assert source.url.startswith("http")
def test_dsac_parse_mock_html():
    source = DSACSource()
    tenders = source.parse_html(MOCK_DSAC_HTML)
    assert len(tenders) == 3
def test_dsac_fetch_uses_fallback_on_empty_or_error():
    source = DSACSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
