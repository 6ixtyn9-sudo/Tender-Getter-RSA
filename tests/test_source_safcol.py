import pytest
from tender_getter.sources.soes.safcol import SAFCOLSource, MOCK_SAFCOL_HTML

def test_safcol_source_initialization():
    source = SAFCOLSource()
    assert source.source_id == "safcol"
    assert source.url.startswith("http")

def test_safcol_parse_mock_html():
    source = SAFCOLSource()
    tenders = source.parse_html(MOCK_SAFCOL_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "SAFCOL/2025/EQ/07"
    assert "Forest Harvesting" in t1.title
    assert t1.required_cidb_class is None
    assert t1.location_target in ["Mpumalanga", "National", "Gauteng", "Western Cape", "Mpumalanga", "Northern Cape"]
    assert t1.closing_date.year == 2026
    t2 = tenders[1]
    assert t2.tender_id == "SAFCOL/2025/ENV/03"
    assert t2.required_cidb_class is None

def test_safcol_fetch_uses_fallback_on_empty_or_error():
    source = SAFCOLSource()
    tenders = source.fetch(html_content="<html><body>No tenders</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "SAFCOL/2025/ENV/03" for t in tenders)
