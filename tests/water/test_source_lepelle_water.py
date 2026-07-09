import pytest
from tender_getter.sources.water.lepelle_water import LepelleWaterSource, MOCK_LEPELLE_WATER_HTML

def test_lepelle_water_source_initialization():
    source = LepelleWaterSource()
    assert source.source_id == "lepelle_water"
    assert source.url.startswith("http")

def test_lepelle_water_parse_mock_html():
    source = LepelleWaterSource()
    tenders = source.parse_html(MOCK_LEPELLE_WATER_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "LNW/2025/CE/11"
    assert "Regional Pipeline Maintenance" in t1.title
    assert t1.required_cidb_class == "CE"
    assert t1.required_cidb_level == 4
    t2 = tenders[1]
    assert t2.tender_id == "LNW/2025/EE/03"
    assert t2.required_cidb_class == "EE"
    assert t2.required_cidb_level == 3

def test_lepelle_water_fetch_uses_fallback_on_empty_or_error():
    source = LepelleWaterSource()
    tenders = source.fetch(html_content="<html><body>No</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "LNW/2025/EE/03" for t in tenders)
