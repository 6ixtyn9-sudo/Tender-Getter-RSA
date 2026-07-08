import pytest
from datetime import datetime, timezone
from tender_getter.sources.provincial.limpopo import LimpopoSource, MOCK_LIMPOPO_HTML

def test_limpopo_source_initialization():
    source = LimpopoSource()
    assert source.source_id == "limpopo_tenders"
    assert source.url.startswith("http")

def test_limpopo_parse_mock_html():
    source = LimpopoSource()
    tenders = source.parse_html(MOCK_LIMPOPO_HTML)
    
    assert len(tenders) == 3
    
    t1 = tenders[0]
    assert t1.tender_id == "LPT/CE/2025/18"
    assert "Water Reticulation" in t1.title
    assert t1.required_cidb_class == "CE"
    assert t1.required_cidb_level == 5
    assert t1.location_target == "Limpopo"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 9
    assert t1.closing_date.day == 11

    t2 = tenders[1]
    assert t2.tender_id == "LPT/GB/2025/04"
    assert t2.required_cidb_class == "GB"
    assert t2.required_cidb_level == 3
    assert t2.location_target == "Limpopo"

def test_limpopo_fetch_uses_fallback_on_empty_or_error():
    source = LimpopoSource()
    tenders = source.fetch(html_content="<html><body>No tenders</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "LPT/GB/2025/04" for t in tenders)
