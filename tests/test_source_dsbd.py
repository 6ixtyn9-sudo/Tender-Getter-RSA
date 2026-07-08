import pytest
from tender_getter.sources.national_depts.dsbd import DSBDSource, MOCK_DSBD_HTML
def test_dsbd_source_initialization():
    source = DSBDSource()
    assert source.source_id == "dsbd"
    assert source.url.startswith("http")
def test_dsbd_parse_mock_html():
    source = DSBDSource()
    tenders = source.parse_html(MOCK_DSBD_HTML)
    assert len(tenders) == 3
def test_dsbd_fetch_uses_fallback_on_empty_or_error():
    source = DSBDSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
