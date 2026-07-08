import pytest
from tender_getter.sources.national_depts.tourism import TourismSource, MOCK_TOURISM_HTML
def test_tourism_source_initialization():
    source = TourismSource()
    assert source.source_id == "tourism_tenders"
    assert source.url.startswith("http")
def test_tourism_parse_mock_html():
    source = TourismSource()
    tenders = source.parse_html(MOCK_TOURISM_HTML)
    assert len(tenders) == 3
def test_tourism_fetch_uses_fallback_on_empty_or_error():
    source = TourismSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
