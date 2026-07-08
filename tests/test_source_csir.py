import pytest
from tender_getter.sources.research.csir import CSIRSource, MOCK_CSIR_HTML
def test_csir_source_initialization():
    source = CSIRSource()
    assert source.source_id == "csir_tenders"
    assert source.url.startswith("http")
def test_csir_parse_mock_html():
    source = CSIRSource()
    tenders = source.parse_html(MOCK_CSIR_HTML)
    assert len(tenders) == 3
def test_csir_fetch_uses_fallback_on_empty_or_error():
    source = CSIRSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
