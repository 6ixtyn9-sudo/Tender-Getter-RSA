import pytest
from datetime import datetime, timezone
from tender_getter.sources.westerncape import WesternCapeSource, MOCK_WESTERNCAPE_HTML
from tender_getter.schemas import TenderOpportunity

def test_westerncape_source_initialization():
    source = WesternCapeSource()
    assert source.source_id == "westerncape_tenders"
    assert "westerncape.gov.za" in source.url

def test_westerncape_parse_mock_html():
    source = WesternCapeSource()
    tenders = source.parse_html(MOCK_WESTERNCAPE_HTML)
    
    assert len(tenders) == 3
    
    # Verify first tender
    t1 = tenders[0]
    assert t1.tender_id == "WCG/2026/012"
    assert "Medical Consumables for Tygerberg Hospital" in t1.title
    assert t1.required_cidb_class is None  # no CIDB class listed in description
    assert t1.required_cidb_level is None
    assert t1.location_target == "Western Cape"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 8
    assert t1.closing_date.day == 30

    # Verify second tender
    t2 = tenders[1]
    assert t2.tender_id == "WCG/2026/045"
    assert t2.required_cidb_class == "GB"
    assert t2.required_cidb_level == 2
    assert t2.location_target == "Western Cape"

def test_westerncape_fetch_uses_fallback_on_empty_or_error():
    source = WesternCapeSource()
    tenders = source.fetch(html_content="<html><body>No tenders or tables here!</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "WCG/2026/045" for t in tenders)
