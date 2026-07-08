import pytest
from datetime import datetime, timezone
from tender_getter.sources.metros.ekurhuleni import EkurhuleniSource, MOCK_EKURHULENI_HTML

def test_ekurhuleni_source_initialization():
    source = EkurhuleniSource()
    assert source.source_id == "ekurhuleni"
    assert source.url.startswith("http")

def test_ekurhuleni_parse_mock_html():
    source = EkurhuleniSource()
    tenders = source.parse_html(MOCK_EKURHULENI_HTML)
    
    assert len(tenders) == 3
    
    # Verify first tender
    t1 = tenders[0]
    assert t1.tender_id == "A-EE-2025-044"
    assert "Airport Precinct Electrical" in t1.title
    assert t1.required_cidb_class == "EE"
    assert t1.required_cidb_level == 4
    assert t1.location_target == "Gauteng"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 9
    assert t1.closing_date.day == 2

    # Verify second tender
    t2 = tenders[1]
    assert t2.tender_id == "A-CE-2025-089"
    assert t2.required_cidb_class == "CE"
    assert t2.required_cidb_level == 7
    assert t2.location_target == "Gauteng"

def test_ekurhuleni_fetch_uses_fallback_on_empty_or_error():
    source = EkurhuleniSource()
    tenders = source.fetch(html_content="<html><body>No tenders or tables here!</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "A-CE-2025-089" for t in tenders)
