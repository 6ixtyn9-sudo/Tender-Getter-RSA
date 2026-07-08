import pytest
from tender_getter.sources.water.overberg_water import OverbergWaterSource, MOCK_OVERBERG_WATER_HTML

def test_overberg_water_source_initialization():
    source = OverbergWaterSource()
    assert source.source_id == "overberg_water"
    assert source.url.startswith("http")

def test_overberg_water_parse_mock_html():
    source = OverbergWaterSource()
    tenders = source.parse_html(MOCK_OVERBERG_WATER_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "OW/2025/CE/06"
    assert "Reservoir Construction" in t1.title
    assert t1.required_cidb_class == "CE"
    assert t1.required_cidb_level == 3
    t2 = tenders[1]
    assert t2.tender_id == "OW/2025/PIPE/02"
    assert t2.required_cidb_class == "CE"
    assert t2.required_cidb_level == 2

def test_overberg_water_fetch_uses_fallback_on_empty_or_error():
    source = OverbergWaterSource()
    tenders = source.fetch(html_content="<html><body>No</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "OW/2025/PIPE/02" for t in tenders)
