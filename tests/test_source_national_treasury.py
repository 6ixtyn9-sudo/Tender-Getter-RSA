import pytest
from tender_getter.sources.national_depts.national_treasury import NationalTreasurySource, MOCK_NATIONAL_TREASURY_HTML
def test_national_treasury_source_initialization():
    source = NationalTreasurySource()
    assert source.source_id == "national_treasury"
    assert source.url.startswith("http")
def test_national_treasury_parse_mock_html():
    source = NationalTreasurySource()
    tenders = source.parse_html(MOCK_NATIONAL_TREASURY_HTML)
    assert len(tenders) == 3
def test_national_treasury_fetch_uses_fallback_on_empty_or_error():
    source = NationalTreasurySource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
