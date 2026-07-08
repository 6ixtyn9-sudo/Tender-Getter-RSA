import pytest
from datetime import datetime, timezone
from tender_getter.sources.cidb import CIDBSource, MOCK_CIDB_HTML
from tender_getter.schemas import TenderOpportunity

def test_cidb_source_initialization():
    source = CIDBSource()
    assert source.source_id == "cidb_itender"
    assert "cidb.org.za" in source.url

def test_cidb_parse_mock_html():
    source = CIDBSource()
    tenders = source.parse_html(MOCK_CIDB_HTML)
    
    assert len(tenders) == 3
    
    # Verify first tender
    t1 = tenders[0]
    assert t1.tender_id == "CIDB/2026/001"
    assert "Water Treatment Works" in t1.title
    assert t1.required_cidb_class == "CE"
    assert t1.required_cidb_level == 6
    assert t1.location_target == "Limpopo"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 8
    assert t1.closing_date.day == 15

    # Verify second tender
    t2 = tenders[1]
    assert t2.tender_id == "CIDB/2026/002"
    assert t2.required_cidb_class == "GB"
    assert t2.required_cidb_level == 5
    assert t2.location_target == "KwaZulu-Natal"

def test_cidb_fetch_uses_fallback_on_empty_or_error():
    source = CIDBSource()
    tenders = source.fetch(html_content="<html><body>No tenders or tables here!</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "CIDB/2026/002" for t in tenders)
