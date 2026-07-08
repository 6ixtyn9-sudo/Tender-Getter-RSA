import pytest
from tender_getter.sources.research.hsrc import HSRCSource, MOCK_HSRC_HTML
def test_hsrc_source_initialization():
    source = HSRCSource()
    assert source.source_id == "hsrc"
    assert source.url.startswith("http")
def test_hsrc_parse_mock_html():
    source = HSRCSource()
    tenders = source.parse_html(MOCK_HSRC_HTML)
    assert len(tenders) == 3
def test_hsrc_fetch_uses_fallback_on_empty_or_error():
    source = HSRCSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
