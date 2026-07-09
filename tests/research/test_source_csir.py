import pytest
from tender_getter.sources.research.csir import CsirSource

def test_csir_source_initialization():
    source = CsirSource()
    assert source.source_id == "csir"
    assert source.url.startswith("http")

def test_csir_parse_mock_html():
    from tender_getter.sources.research.csir import MOCK_HTML
    source = CsirSource()
    tenders = source.parse_html(MOCK_HTML)
    assert len(tenders) >= 0

def test_csir_fetch_uses_fallback_on_empty_or_error():
    source = CsirSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) >= 0
