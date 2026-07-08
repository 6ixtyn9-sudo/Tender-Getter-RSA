import pytest
from tender_getter.sources.national_depts.dod import DoDSource, MOCK_DOD_HTML
def test_dod_source_initialization():
    source = DoDSource()
    assert source.source_id == "dod_tenders"
    assert source.url.startswith("http")
def test_dod_parse_mock_html():
    source = DoDSource()
    tenders = source.parse_html(MOCK_DOD_HTML)
    assert len(tenders) == 3
def test_dod_fetch_uses_fallback_on_empty_or_error():
    source = DoDSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
