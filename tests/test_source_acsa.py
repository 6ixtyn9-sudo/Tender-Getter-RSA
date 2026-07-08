import pytest
from tender_getter.sources.soes.acsa import ACSASource, MOCK_ACSA_HTML

def test_acsa_source_initialization():
    source = ACSASource()
    assert source.source_id == "acsa"
    assert source.url.startswith("http")

def test_acsa_parse_mock_html():
    source = ACSASource()
    tenders = source.parse_html(MOCK_ACSA_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "ACSA/ORT/2025/33"
    assert "Runway Resurfacing" in t1.title
    assert t1.required_cidb_class == "CE"
    assert t1.required_cidb_level == 7
    assert t1.location_target in ["National", "National", "Gauteng", "Western Cape", "Mpumalanga", "Northern Cape"]
    assert t1.closing_date.year == 2026
    t2 = tenders[1]
    assert t2.tender_id == "ACSA/CT/2025/18"
    assert t2.required_cidb_class == "ME"
    assert t2.required_cidb_level == 4

def test_acsa_fetch_uses_fallback_on_empty_or_error():
    source = ACSASource()
    tenders = source.fetch(html_content="<html><body>No tenders</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "ACSA/CT/2025/18" for t in tenders)
