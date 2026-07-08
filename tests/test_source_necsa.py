import pytest
from tender_getter.sources.soes.necsa import NECSASource, MOCK_NECSA_HTML

def test_necsa_source_initialization():
    source = NECSASource()
    assert source.source_id == "necsa"
    assert source.url.startswith("http")

def test_necsa_parse_mock_html():
    source = NECSASource()
    tenders = source.parse_html(MOCK_NECSA_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "NECSA/2025/LAB/06"
    assert "Nuclear Safety" in t1.title
    assert t1.required_cidb_class is None
    assert t1.location_target in ["Gauteng", "National", "Gauteng", "Western Cape", "Mpumalanga", "Northern Cape"]
    assert t1.closing_date.year == 2026
    t2 = tenders[1]
    assert t2.tender_id == "NECSA/2025/HAZ/02"
    assert t2.required_cidb_class is None

def test_necsa_fetch_uses_fallback_on_empty_or_error():
    source = NECSASource()
    tenders = source.fetch(html_content="<html><body>No tenders</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "NECSA/2025/HAZ/02" for t in tenders)
