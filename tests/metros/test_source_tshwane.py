import pytest
from datetime import datetime, timezone
from tender_getter.sources.metros.tshwane import TshwaneSource, MOCK_TSHWANE_HTML

def test_tshwane_source_initialization():
    source = TshwaneSource()
    assert source.source_id == "tshwane"
    assert source.url.startswith("http")

def test_tshwane_parse_mock_html():
    source = TshwaneSource()
    tenders = source.parse_html(MOCK_TSHWANE_HTML)
    
    assert len(tenders) == 3
    
    # Verify first tender
    t1 = tenders[0]
    assert t1.tender_id == "CTMM/EE007/25-26"
    assert "Substation Refurbishment" in t1.title
    assert t1.required_cidb_class == "EE"
    assert t1.required_cidb_level == 4
    assert t1.location_target == "Gauteng"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 8
    assert t1.closing_date.day == 30

    # Verify second tender
    t2 = tenders[1]
    assert t2.tender_id == "CTMM/CE033/25-26"
    assert t2.required_cidb_class == "CE"
    assert t2.required_cidb_level == 5
    assert t2.location_target == "Gauteng"

def test_tshwane_fetch_uses_fallback_on_empty_or_error():
    source = TshwaneSource()
    tenders = source.fetch(html_content="<html><body>No tenders or tables here!</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "CTMM/CE033/25-26" for t in tenders)
