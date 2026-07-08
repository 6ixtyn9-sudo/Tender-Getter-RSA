import pytest
from tender_getter.sources.provincial_depts.gdid import GDIDSource, MOCK_GDID_HTML
def test_gdid_source_initialization():
    source = GDIDSource()
    assert source.source_id == "gdid_tenders"
    assert source.url.startswith("http")
def test_gdid_parse_mock_html():
    source = GDIDSource()
    tenders = source.parse_html(MOCK_GDID_HTML)
    assert len(tenders) == 3
def test_gdid_fetch_uses_fallback_on_empty_or_error():
    source = GDIDSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
