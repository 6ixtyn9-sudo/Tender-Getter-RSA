import pytest
from tender_getter.sources.soes.prasa import PRASASource, MOCK_PRASA_HTML

def test_prasa_source_initialization():
    source = PRASASource()
    assert source.source_id == "prasa"
    assert source.url.startswith("http")

def test_prasa_parse_mock_html():
    source = PRASASource()
    tenders = source.parse_html(MOCK_PRASA_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "PRASA/2025/041"
    assert "Station Cleaning" in t1.title
    assert t1.required_cidb_class is None
    assert t1.location_target in ["Gauteng", "National", "Gauteng", "Western Cape", "Mpumalanga", "Northern Cape"]
    assert t1.closing_date.year == 2026
    t2 = tenders[1]
    assert t2.tender_id == "PRASA/2025/038"
    assert t2.required_cidb_class == "EE"
    assert t2.required_cidb_level == 4

def test_prasa_fetch_uses_fallback_on_empty_or_error():
    source = PRASASource()
    tenders = source.fetch(html_content="<html><body>No tenders</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "PRASA/2025/038" for t in tenders)
