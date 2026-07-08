import pytest
from tender_getter.sources.soes.alexkor import AlexkorSource, MOCK_ALEXKOR_HTML

def test_alexkor_source_initialization():
    source = AlexkorSource()
    assert source.source_id == "alexkor"
    assert source.url.startswith("http")

def test_alexkor_parse_mock_html():
    source = AlexkorSource()
    tenders = source.parse_html(MOCK_ALEXKOR_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "ALEXKOR/2025/MIN/05"
    assert "Diamond Mining Equipment" in t1.title
    assert t1.required_cidb_class is None
    assert t1.location_target in ["Northern Cape", "National", "Gauteng", "Western Cape", "Mpumalanga", "Northern Cape"]
    assert t1.closing_date.year == 2026
    t2 = tenders[1]
    assert t2.tender_id == "ALEXKOR/2025/ENV/02"
    assert t2.required_cidb_class == "CE"
    assert t2.required_cidb_level == 2

def test_alexkor_fetch_uses_fallback_on_empty_or_error():
    source = AlexkorSource()
    tenders = source.fetch(html_content="<html><body>No tenders</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "ALEXKOR/2025/ENV/02" for t in tenders)
