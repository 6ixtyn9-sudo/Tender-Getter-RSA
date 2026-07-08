import pytest
from tender_getter.sources.national_depts.dot import DoTSource, MOCK_DOT_HTML
def test_dot_source_initialization():
    source = DoTSource()
    assert source.source_id == "dot"
    assert source.url.startswith("http")
def test_dot_parse_mock_html():
    source = DoTSource()
    tenders = source.parse_html(MOCK_DOT_HTML)
    assert len(tenders) == 3
def test_dot_fetch_uses_fallback_on_empty_or_error():
    source = DoTSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
