import pytest
from datetime import datetime, timezone
from tender_getter.sources.provincial.northwest import NorthWestSource, MOCK_NORTHWEST_HTML

def test_northwest_source_initialization():
    source = NorthWestSource()
    assert source.source_id == "northwest"
    assert source.url.startswith("http")

def test_northwest_parse_mock_html():
    source = NorthWestSource()
    tenders = source.parse_html(MOCK_NORTHWEST_HTML)
    
    assert len(tenders) == 3
    
    t1 = tenders[0]
    assert t1.tender_id == "NWPT/CE/2025/19"
    assert "Stormwater Drainage" in t1.title
    assert t1.required_cidb_class == "CE"
    assert t1.required_cidb_level == 4
    assert t1.location_target == "North West"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 9
    assert t1.closing_date.day == 7

    t2 = tenders[1]
    assert t2.tender_id == "NWPT/EE/2025/08"
    assert t2.required_cidb_class == "EE"
    assert t2.required_cidb_level == 2
    assert t2.location_target == "North West"

def test_northwest_fetch_uses_fallback_on_empty_or_error():
    source = NorthWestSource()
    tenders = source.fetch(html_content="<html><body>No tenders</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "NWPT/EE/2025/08" for t in tenders)
