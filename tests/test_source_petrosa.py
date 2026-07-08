import pytest
from tender_getter.sources.soes.petrosa import PetroSASource, MOCK_PETROSA_HTML

def test_petrosa_source_initialization():
    source = PetroSASource()
    assert source.source_id == "petrosa_tenders"
    assert source.url.startswith("http")

def test_petrosa_parse_mock_html():
    source = PetroSASource()
    tenders = source.parse_html(MOCK_PETROSA_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "PETROSA/2025/OFF/14"
    assert "Offshore Gas Platform" in t1.title
    assert t1.required_cidb_class == "ME"
    assert t1.required_cidb_level == 7
    assert t1.location_target in ["Western Cape", "National", "Gauteng", "Western Cape", "Mpumalanga", "Northern Cape"]
    assert t1.closing_date.year == 2026
    t2 = tenders[1]
    assert t2.tender_id == "PETROSA/2025/REF/08"
    assert t2.required_cidb_class == "ME"
    assert t2.required_cidb_level == 6

def test_petrosa_fetch_uses_fallback_on_empty_or_error():
    source = PetroSASource()
    tenders = source.fetch(html_content="<html><body>No tenders</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "PETROSA/2025/REF/08" for t in tenders)
