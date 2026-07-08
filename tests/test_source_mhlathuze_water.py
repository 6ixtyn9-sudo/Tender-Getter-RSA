import pytest
from tender_getter.sources.water.mhlathuze_water import MhlathuzeWaterSource, MOCK_MHLATHUZE_WATER_HTML

def test_mhlathuze_water_source_initialization():
    source = MhlathuzeWaterSource()
    assert source.source_id == "mhlathuze_water_tenders"
    assert source.url.startswith("http")

def test_mhlathuze_water_parse_mock_html():
    source = MhlathuzeWaterSource()
    tenders = source.parse_html(MOCK_MHLATHUZE_WATER_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "MW/2025/CE/09"
    assert "Desalination Plant" in t1.title
    assert t1.required_cidb_class == "CE"
    assert t1.required_cidb_level == 4
    t2 = tenders[1]
    assert t2.tender_id == "MW/2025/PIPE/04"
    assert t2.required_cidb_class == "CE"
    assert t2.required_cidb_level == 3

def test_mhlathuze_water_fetch_uses_fallback_on_empty_or_error():
    source = MhlathuzeWaterSource()
    tenders = source.fetch(html_content="<html><body>No</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "MW/2025/PIPE/04" for t in tenders)
