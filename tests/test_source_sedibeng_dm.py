import pytest
from tender_getter.sources.districts.sedibeng_dm import SedibengDMSource, MOCK_SEDIBENG_DM_HTML
def test_sedibeng_dm_source_initialization():
    source = SedibengDMSource()
    assert source.source_id == "sedibeng_dm"
    assert source.url.startswith("http")
def test_sedibeng_dm_parse_mock_html():
    source = SedibengDMSource()
    tenders = source.parse_html(MOCK_SEDIBENG_DM_HTML)
    assert len(tenders) == 3
def test_sedibeng_dm_fetch_uses_fallback_on_empty_or_error():
    source = SedibengDMSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
