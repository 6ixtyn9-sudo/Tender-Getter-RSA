import pytest
from tender_getter.sources.national_depts.cogta import COGTASource, MOCK_COGTA_HTML
def test_cogta_source_initialization():
    source = COGTASource()
    assert source.source_id == "cogta_tenders"
    assert source.url.startswith("http")
def test_cogta_parse_mock_html():
    source = COGTASource()
    tenders = source.parse_html(MOCK_COGTA_HTML)
    assert len(tenders) == 3
def test_cogta_fetch_uses_fallback_on_empty_or_error():
    source = COGTASource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
