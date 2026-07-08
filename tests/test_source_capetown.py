import pytest
from datetime import datetime, timezone
from tender_getter.sources.metros.capetown import CapeTownSource, MOCK_CAPETOWN_HTML
from tender_getter.schemas import TenderOpportunity

def test_capetown_source_initialization():
    source = CapeTownSource()
    assert source.source_id == "capetown_tenders"
    assert "capetown.gov.za" in source.url

def test_capetown_parse_mock_html():
    source = CapeTownSource()
    tenders = source.parse_html(MOCK_CAPETOWN_HTML)
    
    assert len(tenders) == 3
    
    # Verify first tender
    t1 = tenders[0]
    assert t1.tender_id == "282S/2025/26"
    assert "Electrical Grid Maintenance in Khayelitsha" in t1.title
    assert t1.required_cidb_class == "EE"
    assert t1.required_cidb_level == 3
    assert t1.location_target == "Western Cape"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 8
    assert t1.closing_date.day == 30

    # Verify second tender
    t2 = tenders[1]
    assert t2.tender_id == "119Q/2025/26"
    assert t2.required_cidb_class == "CE"
    assert t2.required_cidb_level == 6
    assert t2.location_target == "Western Cape"

def test_capetown_fetch_uses_fallback_on_empty_or_error():
    source = CapeTownSource()
    tenders = source.fetch(html_content="<html><body>No tenders or tables here!</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "119Q/2025/26" for t in tenders)
