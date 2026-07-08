import pytest
from tender_getter.sources.national_depts.dhet import DHETSource, MOCK_DHET_HTML
def test_dhet_source_initialization():
    source = DHETSource()
    assert source.source_id == "dhet_tenders"
    assert source.url.startswith("http")
def test_dhet_parse_mock_html():
    source = DHETSource()
    tenders = source.parse_html(MOCK_DHET_HTML)
    assert len(tenders) == 3
def test_dhet_fetch_uses_fallback_on_empty_or_error():
    source = DHETSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
