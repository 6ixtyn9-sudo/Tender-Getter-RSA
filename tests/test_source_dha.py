import pytest
from tender_getter.sources.national_depts.dha import DHASource, MOCK_DHA_HTML
def test_dha_source_initialization():
    source = DHASource()
    assert source.source_id == "dha_tenders"
    assert source.url.startswith("http")
def test_dha_parse_mock_html():
    source = DHASource()
    tenders = source.parse_html(MOCK_DHA_HTML)
    assert len(tenders) == 3
def test_dha_fetch_uses_fallback_on_empty_or_error():
    source = DHASource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
