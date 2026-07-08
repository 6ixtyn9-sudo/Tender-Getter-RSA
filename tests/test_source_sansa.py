import pytest
from tender_getter.sources.research.sansa import SANSASource, MOCK_SANSA_HTML
def test_sansa_source_initialization():
    source = SANSASource()
    assert source.source_id == "sansa_tenders"
    assert source.url.startswith("http")
def test_sansa_parse_mock_html():
    source = SANSASource()
    tenders = source.parse_html(MOCK_SANSA_HTML)
    assert len(tenders) == 3
def test_sansa_fetch_uses_fallback_on_empty_or_error():
    source = SANSASource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
