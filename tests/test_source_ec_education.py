import pytest
from tender_getter.sources.provincial_depts.ec_education import ECEducationSource, MOCK_EC_EDUCATION_HTML
def test_ec_education_source_initialization():
    source = ECEducationSource()
    assert source.source_id == "ec_education_tenders"
    assert source.url.startswith("http")
def test_ec_education_parse_mock_html():
    source = ECEducationSource()
    tenders = source.parse_html(MOCK_EC_EDUCATION_HTML)
    assert len(tenders) == 3
def test_ec_education_fetch_uses_fallback_on_empty_or_error():
    source = ECEducationSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
