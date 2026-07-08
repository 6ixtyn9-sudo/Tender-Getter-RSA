import pytest
from tender_getter.sources.districts.cape_winelands import CapeWinelandsSource, MOCK_CAPE_WINELANDS_HTML
def test_cape_winelands_source_initialization():
    source = CapeWinelandsSource()
    assert source.source_id == "cape_winelands"
    assert source.url.startswith("http")
def test_cape_winelands_parse_mock_html():
    source = CapeWinelandsSource()
    tenders = source.parse_html(MOCK_CAPE_WINELANDS_HTML)
    assert len(tenders) == 3
def test_cape_winelands_fetch_uses_fallback_on_empty_or_error():
    source = CapeWinelandsSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
