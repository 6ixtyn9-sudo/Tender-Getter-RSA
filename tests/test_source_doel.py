import pytest
from tender_getter.sources.national_depts.doel import DoELSource, MOCK_DOEL_HTML
def test_doel_source_initialization():
    source = DoELSource()
    assert source.source_id == "doel_tenders"
    assert source.url.startswith("http")
def test_doel_parse_mock_html():
    source = DoELSource()
    tenders = source.parse_html(MOCK_DOEL_HTML)
    assert len(tenders) == 3
def test_doel_fetch_uses_fallback_on_empty_or_error():
    source = DoELSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
