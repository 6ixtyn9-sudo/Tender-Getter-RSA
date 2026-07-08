import pytest
from tender_getter.sources.national_depts.dbe import DBESource, MOCK_DBE_HTML
def test_dbe_source_initialization():
    source = DBESource()
    assert source.source_id == "dbe"
    assert source.url.startswith("http")
def test_dbe_parse_mock_html():
    source = DBESource()
    tenders = source.parse_html(MOCK_DBE_HTML)
    assert len(tenders) == 3
def test_dbe_fetch_uses_fallback_on_empty_or_error():
    source = DBESource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
