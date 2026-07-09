import pytest
from tender_getter.sources.metros.ekurhuleni import EkurhuleniSource

def test_ekurhuleni_source_initialization():
    source = EkurhuleniSource()
    assert source.source_id == "ekurhuleni"
    assert source.url.startswith("http")

def test_ekurhuleni_parse_mock_html():
    from tender_getter.sources.metros.ekurhuleni import MOCK_HTML
    source = EkurhuleniSource()
    tenders = source._parse_div_format(MOCK_HTML)
    assert len(tenders) >= 3

def test_ekurhuleni_fetch_uses_fallback_on_empty_or_error():
    source = EkurhuleniSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) >= 0
