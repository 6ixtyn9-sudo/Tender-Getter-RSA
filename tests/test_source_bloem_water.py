import pytest
from tender_getter.sources.water.bloem_water import BloemWaterSource, MOCK_BLOEM_WATER_HTML

def test_bloem_water_source_initialization():
    source = BloemWaterSource()
    assert source.source_id == "bloem_water"
    assert source.url.startswith("http")

def test_bloem_water_parse_mock_html():
    source = BloemWaterSource()
    tenders = source.parse_html(MOCK_BLOEM_WATER_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "BW/2025/LAB/04"
    assert "Water Quality Laboratory" in t1.title
    assert t1.required_cidb_class is None
    t2 = tenders[1]
    assert t2.tender_id == "BW/2025/CE/09"
    assert t2.required_cidb_class == "CE"
    assert t2.required_cidb_level == 3

def test_bloem_water_fetch_uses_fallback_on_empty_or_error():
    source = BloemWaterSource()
    tenders = source.fetch(html_content="<html><body>No</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "BW/2025/CE/09" for t in tenders)
