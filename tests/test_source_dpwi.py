import pytest
from tender_getter.sources.national_depts.dpwi import DPWISource, MOCK_DPWI_HTML
def test_dpwi_source_initialization():
    source = DPWISource()
    assert source.source_id == "dpwi_tenders"
    assert source.url.startswith("http")
def test_dpwi_parse_mock_html():
    source = DPWISource()
    tenders = source.parse_html(MOCK_DPWI_HTML)
    assert len(tenders) == 3
def test_dpwi_fetch_uses_fallback_on_empty_or_error():
    source = DPWISource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
