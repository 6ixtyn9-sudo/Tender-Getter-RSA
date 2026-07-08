import pytest
from datetime import datetime, timezone
from tender_getter.sources.provincial.mpumalanga import MpumalangaSource, MOCK_MPUMALANGA_HTML

def test_mpumalanga_source_initialization():
    source = MpumalangaSource()
    assert source.source_id == "mpumalanga"
    assert source.url.startswith("http")

def test_mpumalanga_parse_mock_html():
    source = MpumalangaSource()
    tenders = source.parse_html(MOCK_MPUMALANGA_HTML)
    
    assert len(tenders) == 3
    
    t1 = tenders[0]
    assert t1.tender_id == "MPT/CE/2025/27"
    assert "Road Resurfacing" in t1.title
    assert t1.required_cidb_class == "CE"
    assert t1.required_cidb_level == 6
    assert t1.location_target == "Mpumalanga"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 9
    assert t1.closing_date.day == 16

    t2 = tenders[1]
    assert t2.tender_id == "MPT/EE/2025/14"
    assert t2.required_cidb_class == "EE"
    assert t2.required_cidb_level == 4
    assert t2.location_target == "Mpumalanga"

def test_mpumalanga_fetch_uses_fallback_on_empty_or_error():
    source = MpumalangaSource()
    tenders = source.fetch(html_content="<html><body>No tenders</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "MPT/EE/2025/14" for t in tenders)
