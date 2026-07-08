import pytest
from tender_getter.sources.national_depts.dmre import DMRESource, MOCK_DMRE_HTML
def test_dmre_source_initialization():
    source = DMRESource()
    assert source.source_id == "dmre"
    assert source.url.startswith("http")
def test_dmre_parse_mock_html():
    source = DMRESource()
    tenders = source.parse_html(MOCK_DMRE_HTML)
    assert len(tenders) == 3
def test_dmre_fetch_uses_fallback_on_empty_or_error():
    source = DMRESource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
