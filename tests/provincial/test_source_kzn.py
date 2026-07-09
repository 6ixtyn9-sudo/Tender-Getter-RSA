import pytest
from datetime import datetime, timezone
from tender_getter.sources.provincial.kzn import KZNSource, MOCK_KZN_HTML
from tender_getter.schemas import TenderOpportunity

def test_kzn_source_initialization():
    source = KZNSource()
    assert source.source_id == "kzn_treasury"
    assert "kzntreasury.gov.za" in source.url

def test_kzn_parse_mock_html():
    source = KZNSource()
    tenders = source.parse_html(MOCK_KZN_HTML)
    
    assert len(tenders) == 3
    
    # Verify first tender
    t1 = tenders[0]
    assert t1.tender_id == "BID KZN/2026/012"
    assert "Refurbishment of Public Schools in Umlazi" in t1.title
    assert t1.required_cidb_class == "GB"
    assert t1.required_cidb_level == 4
    assert t1.location_target == "KwaZulu-Natal"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 8
    assert t1.closing_date.day == 30

    # Verify second tender
    t2 = tenders[1]
    assert t2.tender_id == "BID KZN/2026/045"
    assert t2.required_cidb_class is None  # no construction requirements
    assert t2.required_cidb_level is None
    assert t2.location_target == "KwaZulu-Natal"

def test_kzn_fetch_uses_fallback_on_empty_or_error():
    source = KZNSource()
    tenders = source.fetch(html_content="<html><body>No tenders or tables here!</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "BID KZN/2026/089" for t in tenders)
