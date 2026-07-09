import pytest
from tender_getter.sources.soes.landbank import LandbankSource, MOCK_LANDBANK_HTML

def test_landbank_source_initialization():
    source = LandbankSource()
    assert source.source_id == "landbank"
    assert source.url.startswith("http")

def test_landbank_parse_mock_html():
    source = LandbankSource()
    tenders = source.parse_html(MOCK_LANDBANK_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "LB/2025/ICT/07"
    assert "Core Banking Software" in t1.title
    assert t1.required_cidb_class is None
    assert t1.location_target in ["National", "National", "Gauteng", "Western Cape", "Mpumalanga", "Northern Cape"]
    assert t1.closing_date.year == 2026
    t2 = tenders[1]
    assert t2.tender_id == "LB/2025/AUDIT/03"
    assert t2.required_cidb_class is None

def test_landbank_fetch_uses_fallback_on_empty_or_error():
    source = LandbankSource()
    tenders = source.fetch(html_content="<html><body>No tenders</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "LB/2025/AUDIT/03" for t in tenders)
