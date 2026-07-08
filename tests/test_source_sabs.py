import pytest
from tender_getter.sources.research.sabs import SABSSource, MOCK_SABS_HTML
def test_sabs_source_initialization():
    source = SABSSource()
    assert source.source_id == "sabs_tenders"
    assert source.url.startswith("http")
def test_sabs_parse_mock_html():
    source = SABSSource()
    tenders = source.parse_html(MOCK_SABS_HTML)
    assert len(tenders) == 3
def test_sabs_fetch_uses_fallback_on_empty_or_error():
    source = SABSSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
