import pytest
from datetime import datetime, timezone
from tender_getter.sources.gauteng import GautengSource, MOCK_GAUTENG_HTML
from tender_getter.schemas import TenderOpportunity

def test_gauteng_source_initialization():
    source = GautengSource()
    assert source.source_id == "gauteng_etenders"
    assert "gauteng.gov.za" in source.url

def test_gauteng_parse_mock_html():
    source = GautengSource()
    tenders = source.parse_html(MOCK_GAUTENG_HTML)
    
    assert len(tenders) == 3
    
    # Verify first tender
    t1 = tenders[0]
    assert t1.tender_id == "GT/GDSD/045/2026"
    assert "Supply and Delivery of Food Parcels" in t1.title
    assert t1.required_cidb_class == "GB"
    assert t1.required_cidb_level == 1
    assert t1.location_target == "Gauteng"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 8
    assert t1.closing_date.day == 15

    # Verify second tender
    t2 = tenders[1]
    assert t2.tender_id == "GT/GDID/089/2026"
    assert t2.required_cidb_class == "GB"
    assert t2.required_cidb_level == 6
    assert t2.location_target == "Gauteng"

def test_gauteng_fetch_uses_fallback_on_empty_or_error():
    source = GautengSource()
    tenders = source.fetch(html_content="<html><body>No tenders or tables here!</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "GT/GDID/089/2026" for t in tenders)
