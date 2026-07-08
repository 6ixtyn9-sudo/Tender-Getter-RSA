import pytest
from tender_getter.sources.districts.or_tambo import ORTamboSource, MOCK_OR_TAMBO_HTML
def test_or_tambo_source_initialization():
    source = ORTamboSource()
    assert source.source_id == "or_tambo_tenders"
    assert source.url.startswith("http")
def test_or_tambo_parse_mock_html():
    source = ORTamboSource()
    tenders = source.parse_html(MOCK_OR_TAMBO_HTML)
    assert len(tenders) == 3
def test_or_tambo_fetch_uses_fallback_on_empty_or_error():
    source = ORTamboSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
