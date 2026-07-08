import pytest
from tender_getter.sources.water.sedibeng_water import SedibengWaterSource, MOCK_SEDIBENG_WATER_HTML

def test_sedibeng_water_source_initialization():
    source = SedibengWaterSource()
    assert source.source_id == "sedibeng_water"
    assert source.url.startswith("http")

def test_sedibeng_water_parse_mock_html():
    source = SedibengWaterSource()
    tenders = source.parse_html(MOCK_SEDIBENG_WATER_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "SEDW/2025/CE/07"
    assert "Pump Station Repairs" in t1.title
    assert t1.required_cidb_class == "CE"
    assert t1.required_cidb_level == 3
    t2 = tenders[1]
    assert t2.tender_id == "SEDW/2025/PIPE/03"
    assert t2.required_cidb_class == "CE"
    assert t2.required_cidb_level == 2

def test_sedibeng_water_fetch_uses_fallback_on_empty_or_error():
    source = SedibengWaterSource()
    tenders = source.fetch(html_content="<html><body>No</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "SEDW/2025/PIPE/03" for t in tenders)
