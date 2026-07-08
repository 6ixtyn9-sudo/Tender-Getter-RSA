import pytest
from tender_getter.sources.national_depts.dhs import DHSSource, MOCK_DHS_HTML
def test_dhs_source_initialization():
    source = DHSSource()
    assert source.source_id == "dhs_tenders"
    assert source.url.startswith("http")
def test_dhs_parse_mock_html():
    source = DHSSource()
    tenders = source.parse_html(MOCK_DHS_HTML)
    assert len(tenders) == 3
def test_dhs_fetch_uses_fallback_on_empty_or_error():
    source = DHSSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
