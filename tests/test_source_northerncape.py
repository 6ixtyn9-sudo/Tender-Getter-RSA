import pytest
from datetime import datetime, timezone
from tender_getter.sources.provincial.northerncape import NorthernCapeSource, MOCK_NORTHERNCAPE_HTML

def test_northerncape_source_initialization():
    source = NorthernCapeSource()
    assert source.source_id == "northerncape_tenders"
    assert source.url.startswith("http")

def test_northerncape_parse_mock_html():
    source = NorthernCapeSource()
    tenders = source.parse_html(MOCK_NORTHERNCAPE_HTML)
    
    assert len(tenders) == 3
    
    t1 = tenders[0]
    assert t1.tender_id == "NCPT/CE/2025/15"
    assert "Desert Road Maintenance" in t1.title
    assert t1.required_cidb_class == "CE"
    assert t1.required_cidb_level == 3
    assert t1.location_target == "Northern Cape"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 9
    assert t1.closing_date.day == 13

    t2 = tenders[1]
    assert t2.tender_id == "NCPT/EE/2025/05"
    assert t2.required_cidb_class == "EE"
    assert t2.required_cidb_level == 2
    assert t2.location_target == "Northern Cape"

def test_northerncape_fetch_uses_fallback_on_empty_or_error():
    source = NorthernCapeSource()
    tenders = source.fetch(html_content="<html><body>No tenders</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "NCPT/EE/2025/05" for t in tenders)
