import pytest
from tender_getter.sources.water.rand_water import RandWaterSource, MOCK_RAND_WATER_HTML

def test_rand_water_source_initialization():
    source = RandWaterSource()
    assert source.source_id == "rand_water"
    assert source.url.startswith("http")

def test_rand_water_parse_mock_html():
    source = RandWaterSource()
    tenders = source.parse_html(MOCK_RAND_WATER_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "RW/2025/CE/14"
    assert "Bulk Water Pipeline" in t1.title
    assert t1.required_cidb_class == "CE"
    assert t1.required_cidb_level == 6
    t2 = tenders[1]
    assert t2.tender_id == "RW/2025/EE/05"
    assert t2.required_cidb_class == "EE"
    assert t2.required_cidb_level == 4

def test_rand_water_fetch_uses_fallback_on_empty_or_error():
    source = RandWaterSource()
    tenders = source.fetch(html_content="<html><body>No</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "RW/2025/EE/05" for t in tenders)
