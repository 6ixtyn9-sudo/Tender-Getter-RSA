import pytest
from tender_getter.sources.soes.atns import ATNSSource, MOCK_ATNS_HTML

def test_atns_source_initialization():
    source = ATNSSource()
    assert source.source_id == "atns_tenders"
    assert source.url.startswith("http")

def test_atns_parse_mock_html():
    source = ATNSSource()
    tenders = source.parse_html(MOCK_ATNS_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "ATNS/2025/RADAR/07"
    assert "Radar System Maintenance" in t1.title
    assert t1.required_cidb_class == "EE"
    assert t1.required_cidb_level == 4
    assert t1.location_target in ["Gauteng", "National", "Gauteng", "Western Cape", "Mpumalanga", "Northern Cape"]
    assert t1.closing_date.year == 2026
    t2 = tenders[1]
    assert t2.tender_id == "ATNS/2025/ATC/12"
    assert t2.required_cidb_class is None

def test_atns_fetch_uses_fallback_on_empty_or_error():
    source = ATNSSource()
    tenders = source.fetch(html_content="<html><body>No tenders</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "ATNS/2025/ATC/12" for t in tenders)
