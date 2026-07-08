import pytest
from tender_getter.sources.national_depts.dpme import DPMESource, MOCK_DPME_HTML
def test_dpme_source_initialization():
    source = DPMESource()
    assert source.source_id == "dpme"
    assert source.url.startswith("http")
def test_dpme_parse_mock_html():
    source = DPMESource()
    tenders = source.parse_html(MOCK_DPME_HTML)
    assert len(tenders) == 3
def test_dpme_fetch_uses_fallback_on_empty_or_error():
    source = DPMESource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
