import pytest
from tender_getter.sources.dfi.compensation_fund import CompensationFundSource, MOCK_COMPENSATION_FUND_HTML

def test_compensation_fund_source_initialization():
    source = CompensationFundSource()
    assert source.source_id == "compensation_fund"
    assert source.url.startswith("http")

def test_compensation_fund_parse_mock_html():
    source = CompensationFundSource()
    tenders = source.parse_html(MOCK_COMPENSATION_FUND_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "CF/2025/ICT/06"
    assert "Injury Claim" in t1.title

def test_compensation_fund_fetch_uses_fallback_on_empty_or_error():
    source = CompensationFundSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "CF/2025/MED/03" for t in tenders)
