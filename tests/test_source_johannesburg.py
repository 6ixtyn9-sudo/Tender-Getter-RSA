import pytest
from datetime import datetime, timezone
from tender_getter.sources.metros.johannesburg import JohannesburgSource, MOCK_JOHANNESBURG_HTML
from tender_getter.schemas import TenderOpportunity

def test_johannesburg_source_initialization():
    source = JohannesburgSource()
    assert source.source_id == "johannesburg_tenders"
    assert "joburg.org.za" in source.url

def test_johannesburg_parse_mock_html():
    source = JohannesburgSource()
    tenders = source.parse_html(MOCK_JOHANNESBURG_HTML)
    
    assert len(tenders) == 3
    
    # Verify first tender
    t1 = tenders[0]
    assert t1.tender_id == "COJ/EE001/25-26"
    assert "Electrical Grid Upgrades" in t1.title
    assert t1.required_cidb_class == "EE"
    assert t1.required_cidb_level == 4
    assert t1.location_target == "Gauteng"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 8
    assert t1.closing_date.day == 28

    # Verify second tender
    t2 = tenders[1]
    assert t2.tender_id == "COJ/CE015/25-26"
    assert t2.required_cidb_class == "CE"
    assert t2.required_cidb_level == 6
    assert t2.location_target == "Gauteng"

def test_johannesburg_fetch_uses_fallback_on_empty_or_error():
    source = JohannesburgSource()
    tenders = source.fetch(html_content="<html><body>No tenders or tables here!</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "COJ/CE015/25-26" for t in tenders)
