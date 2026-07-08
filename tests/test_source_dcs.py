import pytest
from tender_getter.sources.national_depts.dcs import DCSSource, MOCK_DCS_HTML
def test_dcs_source_initialization():
    source = DCSSource()
    assert source.source_id == "dcs_tenders"
    assert source.url.startswith("http")
def test_dcs_parse_mock_html():
    source = DCSSource()
    tenders = source.parse_html(MOCK_DCS_HTML)
    assert len(tenders) == 3
def test_dcs_fetch_uses_fallback_on_empty_or_error():
    source = DCSSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
