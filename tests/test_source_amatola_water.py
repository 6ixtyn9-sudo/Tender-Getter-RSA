import pytest
from tender_getter.sources.water.amatola_water import AmatolaWaterSource, MOCK_AMATOLA_WATER_HTML

def test_amatola_water_source_initialization():
    source = AmatolaWaterSource()
    assert source.source_id == "amatola_water"
    assert source.url.startswith("http")

def test_amatola_water_parse_mock_html():
    source = AmatolaWaterSource()
    tenders = source.parse_html(MOCK_AMATOLA_WATER_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "AW/2025/CE/13"
    assert "Community Water Scheme" in t1.title
    assert t1.required_cidb_class == "CE"
    assert t1.required_cidb_level == 3
    t2 = tenders[1]
    assert t2.tender_id == "AW/2025/EE/04"
    assert t2.required_cidb_class == "EE"
    assert t2.required_cidb_level == 2

def test_amatola_water_fetch_uses_fallback_on_empty_or_error():
    source = AmatolaWaterSource()
    tenders = source.fetch(html_content="<html><body>No</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "AW/2025/EE/04" for t in tenders)
