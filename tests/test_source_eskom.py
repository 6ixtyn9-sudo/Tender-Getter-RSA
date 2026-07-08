import pytest
from datetime import datetime, timezone
from tender_getter.sources.soes.eskom import EskomSource, MOCK_ESKOM_HTML
from tender_getter.schemas import TenderOpportunity

def test_eskom_source_initialization():
    source = EskomSource()
    assert source.source_id == "eskom_tenders"
    assert "eskom.co.za" in source.url

def test_eskom_parse_mock_html():
    source = EskomSource()
    tenders = source.parse_html(MOCK_ESKOM_HTML)
    
    assert len(tenders) == 3
    
    # Verify first tender
    t1 = tenders[0]
    assert t1.tender_id == "E3110DXGPOU"
    assert "Provision of Lv Maintenance" in t1.title
    assert t1.required_cidb_class == "EE"
    assert t1.required_cidb_level == 4
    assert t1.location_target == "Gauteng"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 7
    assert t1.closing_date.day == 31

    # Verify second tender
    t2 = tenders[1]
    assert t2.tender_id == "E3043GXMPMAT"
    assert t2.required_cidb_class == "ME"
    assert t2.required_cidb_level == 3
    assert t2.location_target == "Mpumalanga"

def test_eskom_fetch_uses_fallback_on_empty_or_error():
    source = EskomSource()
    tenders = source.fetch(html_content="<html><body>No tenders or tables here!</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "E3043GXMPMAT" for t in tenders)
