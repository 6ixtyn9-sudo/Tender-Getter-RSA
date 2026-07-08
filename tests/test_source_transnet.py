import pytest
from datetime import datetime, timezone
from tender_getter.sources.soes.transnet import TransnetSource, MOCK_TRANSNET_HTML
from tender_getter.schemas import TenderOpportunity

def test_transnet_source_initialization():
    source = TransnetSource()
    assert source.source_id == "transnet"
    assert "transnetetenders" in source.url

def test_transnet_parse_mock_html():
    source = TransnetSource()
    tenders = source.parse_html(MOCK_TRANSNET_HTML)
    
    assert len(tenders) == 3
    
    # Verify first tender
    t1 = tenders[0]
    assert t1.tender_id == "TE/2026/06/0012/RFP"
    assert "Refurbishment of Freight Locomotives" in t1.title
    assert t1.required_cidb_class == "ME"
    assert t1.required_cidb_level == 6
    assert t1.location_target == "Western Cape"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 8
    assert t1.closing_date.day == 30

    # Verify second tender
    t2 = tenders[1]
    assert t2.tender_id == "TNPA/2026/06/0002/RFP"
    assert t2.required_cidb_class == "ME"
    assert t2.required_cidb_level == 5
    assert t2.location_target == "KwaZulu-Natal"

def test_transnet_fetch_uses_fallback_on_empty_or_error():
    source = TransnetSource()
    tenders = source.fetch(html_content="<html><body>No tenders or tables here!</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "TNPA/2026/06/0002/RFP" for t in tenders)
