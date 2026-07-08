import pytest
from tender_getter.sources.provincial_depts.kzn_dot import KZNDoTSource, MOCK_KZN_DOT_HTML
def test_kzn_dot_source_initialization():
    source = KZNDoTSource()
    assert source.source_id == "kzn_dot_tenders"
    assert source.url.startswith("http")
def test_kzn_dot_parse_mock_html():
    source = KZNDoTSource()
    tenders = source.parse_html(MOCK_KZN_DOT_HTML)
    assert len(tenders) == 3
def test_kzn_dot_fetch_uses_fallback_on_empty_or_error():
    source = KZNDoTSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
