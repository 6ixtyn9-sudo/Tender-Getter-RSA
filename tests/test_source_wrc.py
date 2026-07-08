import pytest
from tender_getter.sources.research.wrc import WRCSource, MOCK_WRC_HTML
def test_wrc_source_initialization():
    source = WRCSource()
    assert source.source_id == "wrc_tenders"
    assert source.url.startswith("http")
def test_wrc_parse_mock_html():
    source = WRCSource()
    tenders = source.parse_html(MOCK_WRC_HTML)
    assert len(tenders) == 3
def test_wrc_fetch_uses_fallback_on_empty_or_error():
    source = WRCSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
