import pytest
from datetime import datetime, timezone
from tender_getter.sources.metros.nelson_mandela_bay import NelsonMandelaBaySource, MOCK_NELSONMANDELABAY_HTML

def test_nelson_mandela_bay_source_initialization():
    source = NelsonMandelaBaySource()
    assert source.source_id == "nelsonmandelabay_tenders"
    assert source.url.startswith("http")

def test_nelson_mandela_bay_parse_mock_html():
    source = NelsonMandelaBaySource()
    tenders = source.parse_html(MOCK_NELSONMANDELABAY_HTML)
    
    assert len(tenders) == 3
    
    # Verify first tender
    t1 = tenders[0]
    assert t1.tender_id == "NMB/CE/2025/14"
    assert "Coastal Road Resurfacing" in t1.title
    assert t1.required_cidb_class == "CE"
    assert t1.required_cidb_level == 5
    assert t1.location_target == "Eastern Cape"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 9
    assert t1.closing_date.day == 8

    # Verify second tender
    t2 = tenders[1]
    assert t2.tender_id == "NMB/EE/2025/06"
    assert t2.required_cidb_class == "EE"
    assert t2.required_cidb_level == 3
    assert t2.location_target == "Eastern Cape"

def test_nelson_mandela_bay_fetch_uses_fallback_on_empty_or_error():
    source = NelsonMandelaBaySource()
    tenders = source.fetch(html_content="<html><body>No tenders or tables here!</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "NMB/EE/2025/06" for t in tenders)
