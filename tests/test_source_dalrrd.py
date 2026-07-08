import pytest
from tender_getter.sources.national_depts.dalrrd import DALRRDSource, MOCK_DALRRD_HTML
def test_dalrrd_source_initialization():
    source = DALRRDSource()
    assert source.source_id == "dalrrd_tenders"
    assert source.url.startswith("http")
def test_dalrrd_parse_mock_html():
    source = DALRRDSource()
    tenders = source.parse_html(MOCK_DALRRD_HTML)
    assert len(tenders) == 3
def test_dalrrd_fetch_uses_fallback_on_empty_or_error():
    source = DALRRDSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
