import pytest
from tender_getter.sources.national_depts.saps import SAPSSource, MOCK_SAPS_HTML
def test_saps_source_initialization():
    source = SAPSSource()
    assert source.source_id == "saps"
    assert source.url.startswith("http")
def test_saps_parse_mock_html():
    source = SAPSSource()
    tenders = source.parse_html(MOCK_SAPS_HTML)
    assert len(tenders) == 3
def test_saps_fetch_uses_fallback_on_empty_or_error():
    source = SAPSSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
