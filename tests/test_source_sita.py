import pytest
from datetime import datetime, timezone
from tender_getter.sources.research.sita import SITASource, MOCK_SITA_HTML
from tender_getter.schemas import TenderOpportunity

def test_sita_source_initialization():
    source = SITASource()
    assert source.source_id == "sita"
    assert "sita.co.za" in source.url

def test_sita_parse_mock_html():
    source = SITASource()
    tenders = source.parse_html(MOCK_SITA_HTML)
    
    assert len(tenders) == 3
    
    # Verify first tender
    t1 = tenders[0]
    assert t1.tender_id == "RFB 2026/012"
    assert "Cloud Hosting and Infrastructure Services" in t1.title
    assert t1.required_cidb_class is None  # IT tender, no construction grade
    assert t1.location_target is None  # "National" doesn't hit province_from_text map
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 8
    assert t1.closing_date.day == 30

    # Verify second tender
    t2 = tenders[1]
    assert t2.tender_id == "RFB 2026/045"
    assert "Supply, Delivery, and Maintenance of Desktops" in t2.title
    assert t2.location_target == "Western Cape"

def test_sita_fetch_uses_fallback_on_empty_or_error():
    source = SITASource()
    tenders = source.fetch(html_content="<html><body>No tenders or tables here!</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "RFB 2026/045" for t in tenders)
