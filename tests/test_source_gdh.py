import pytest
from tender_getter.sources.provincial_depts.gdh import GDHSource, MOCK_GDH_HTML
def test_gdh_source_initialization():
    source = GDHSource()
    assert source.source_id == "gdh_tenders"
    assert source.url.startswith("http")
def test_gdh_parse_mock_html():
    source = GDHSource()
    tenders = source.parse_html(MOCK_GDH_HTML)
    assert len(tenders) == 3
def test_gdh_fetch_uses_fallback_on_empty_or_error():
    source = GDHSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
