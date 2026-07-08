import pytest
from datetime import datetime, timezone
from tender_getter.sources.metros.buffalo_city import BuffaloCitySource, MOCK_BUFFALOCITY_HTML

def test_buffalo_city_source_initialization():
    source = BuffaloCitySource()
    assert source.source_id == "buffalo_city"
    assert source.url.startswith("http")

def test_buffalo_city_parse_mock_html():
    source = BuffaloCitySource()
    tenders = source.parse_html(MOCK_BUFFALOCITY_HTML)
    
    assert len(tenders) == 3
    
    # Verify first tender
    t1 = tenders[0]
    assert t1.tender_id == "BCMM/CE/045/2025"
    assert "Rural Gravel Road Upgrade" in t1.title
    assert t1.required_cidb_class == "CE"
    assert t1.required_cidb_level == 4
    assert t1.location_target == "Eastern Cape"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 9
    assert t1.closing_date.day == 12

    # Verify second tender
    t2 = tenders[1]
    assert t2.tender_id == "BCMM/EE/012/2025"
    assert t2.required_cidb_class == "EE"
    assert t2.required_cidb_level == 3
    assert t2.location_target == "Eastern Cape"

def test_buffalo_city_fetch_uses_fallback_on_empty_or_error():
    source = BuffaloCitySource()
    tenders = source.fetch(html_content="<html><body>No tenders or tables here!</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "BCMM/EE/012/2025" for t in tenders)
