import pytest
from tender_getter.sources.provincial_depts.ec_public_works import ECPublicWorksSource, MOCK_EC_PUBLIC_WORKS_HTML
def test_ec_public_works_source_initialization():
    source = ECPublicWorksSource()
    assert source.source_id == "ec_public_works"
    assert source.url.startswith("http")
def test_ec_public_works_parse_mock_html():
    source = ECPublicWorksSource()
    tenders = source.parse_html(MOCK_EC_PUBLIC_WORKS_HTML)
    assert len(tenders) == 3
def test_ec_public_works_fetch_uses_fallback_on_empty_or_error():
    source = ECPublicWorksSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
