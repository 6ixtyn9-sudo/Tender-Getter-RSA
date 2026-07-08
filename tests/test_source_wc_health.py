import pytest
from tender_getter.sources.provincial_depts.wc_health import WCHealthSource, MOCK_WC_HEALTH_HTML
def test_wc_health_source_initialization():
    source = WCHealthSource()
    assert source.source_id == "wc_health_tenders"
    assert source.url.startswith("http")
def test_wc_health_parse_mock_html():
    source = WCHealthSource()
    tenders = source.parse_html(MOCK_WC_HEALTH_HTML)
    assert len(tenders) == 3
def test_wc_health_fetch_uses_fallback_on_empty_or_error():
    source = WCHealthSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
