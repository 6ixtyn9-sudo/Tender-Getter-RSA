import pytest
from tender_getter.sources.national_depts.dtic import DTICSource, MOCK_DTIC_HTML
def test_dtic_source_initialization():
    source = DTICSource()
    assert source.source_id == "dtic"
    assert source.url.startswith("http")
def test_dtic_parse_mock_html():
    source = DTICSource()
    tenders = source.parse_html(MOCK_DTIC_HTML)
    assert len(tenders) == 3
def test_dtic_fetch_uses_fallback_on_empty_or_error():
    source = DTICSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
