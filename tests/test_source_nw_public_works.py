import pytest
from tender_getter.sources.provincial_depts.nw_public_works import NWPublicWorksSource, MOCK_NW_PUBLIC_WORKS_HTML
def test_nw_public_works_source_initialization():
    source = NWPublicWorksSource()
    assert source.source_id == "nw_public_works"
    assert source.url.startswith("http")
def test_nw_public_works_parse_mock_html():
    source = NWPublicWorksSource()
    tenders = source.parse_html(MOCK_NW_PUBLIC_WORKS_HTML)
    assert len(tenders) == 3
def test_nw_public_works_fetch_uses_fallback_on_empty_or_error():
    source = NWPublicWorksSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
