import pytest
from tender_getter.sources.districts.ilembe import ILembeSource, MOCK_ILEMBE_HTML
def test_ilembe_source_initialization():
    source = ILembeSource()
    assert source.source_id == "ilembe_tenders"
    assert source.url.startswith("http")
def test_ilembe_parse_mock_html():
    source = ILembeSource()
    tenders = source.parse_html(MOCK_ILEMBE_HTML)
    assert len(tenders) == 3
def test_ilembe_fetch_uses_fallback_on_empty_or_error():
    source = ILembeSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
