import pytest
from tender_getter.sources.research.geoscience import GeoscienceSource, MOCK_GEOSCIENCE_HTML
def test_geoscience_source_initialization():
    source = GeoscienceSource()
    assert source.source_id == "geoscience"
    assert source.url.startswith("http")
def test_geoscience_parse_mock_html():
    source = GeoscienceSource()
    tenders = source.parse_html(MOCK_GEOSCIENCE_HTML)
    assert len(tenders) == 3
def test_geoscience_fetch_uses_fallback_on_empty_or_error():
    source = GeoscienceSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
