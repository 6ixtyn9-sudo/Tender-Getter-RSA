import pytest
from tender_getter.sources.soes.denel import DenelSource, MOCK_DENEL_HTML

def test_denel_source_initialization():
    source = DenelSource()
    assert source.source_id == "denel"
    assert source.url.startswith("http")

def test_denel_parse_mock_html():
    source = DenelSource()
    tenders = source.parse_html(MOCK_DENEL_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "DENEL/2025/MFG/12"
    assert "Precision Component" in t1.title
    assert t1.required_cidb_class == "ME"
    assert t1.required_cidb_level == 4
    assert t1.location_target in ["Gauteng", "National", "Gauteng", "Western Cape", "Mpumalanga", "Northern Cape"]
    assert t1.closing_date.year == 2026
    t2 = tenders[1]
    assert t2.tender_id == "DENEL/2025/ICT/04"
    assert t2.required_cidb_class is None

def test_denel_fetch_uses_fallback_on_empty_or_error():
    source = DenelSource()
    tenders = source.fetch(html_content="<html><body>No tenders</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "DENEL/2025/ICT/04" for t in tenders)
