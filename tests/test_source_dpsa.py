import pytest
from tender_getter.sources.national_depts.dpsa import DPSASource, MOCK_DPSA_HTML
def test_dpsa_source_initialization():
    source = DPSASource()
    assert source.source_id == "dpsa"
    assert source.url.startswith("http")
def test_dpsa_parse_mock_html():
    source = DPSASource()
    tenders = source.parse_html(MOCK_DPSA_HTML)
    assert len(tenders) == 3
def test_dpsa_fetch_uses_fallback_on_empty_or_error():
    source = DPSASource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
