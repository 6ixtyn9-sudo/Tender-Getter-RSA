import pytest
from tender_getter.sources.research.mintek import MintekSource, MOCK_MINTEK_HTML
def test_mintek_source_initialization():
    source = MintekSource()
    assert source.source_id == "mintek"
    assert source.url.startswith("http")
def test_mintek_parse_mock_html():
    source = MintekSource()
    tenders = source.parse_html(MOCK_MINTEK_HTML)
    assert len(tenders) == 3
def test_mintek_fetch_uses_fallback_on_empty_or_error():
    source = MintekSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
