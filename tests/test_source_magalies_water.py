import pytest
from tender_getter.sources.water.magalies_water import MagaliesWaterSource, MOCK_MAGALIES_WATER_HTML

def test_magalies_water_source_initialization():
    source = MagaliesWaterSource()
    assert source.source_id == "magalies_water"
    assert source.url.startswith("http")

def test_magalies_water_parse_mock_html():
    source = MagaliesWaterSource()
    tenders = source.parse_html(MOCK_MAGALIES_WATER_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "MAGW/2025/CE/08"
    assert "Reservoir Construction" in t1.title
    assert t1.required_cidb_class == "CE"
    assert t1.required_cidb_level == 4
    t2 = tenders[1]
    assert t2.tender_id == "MAGW/2025/PIPE/05"
    assert t2.required_cidb_class == "CE"
    assert t2.required_cidb_level == 2

def test_magalies_water_fetch_uses_fallback_on_empty_or_error():
    source = MagaliesWaterSource()
    tenders = source.fetch(html_content="<html><body>No</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "MAGW/2025/PIPE/05" for t in tenders)
