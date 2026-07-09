import pytest
from tender_getter.sources.water.umgeni_water import UmgeniWaterSource, MOCK_UMGENI_WATER_HTML

def test_umgeni_water_source_initialization():
    source = UmgeniWaterSource()
    assert source.source_id == "umgeni_water"
    assert source.url.startswith("http")

def test_umgeni_water_parse_mock_html():
    source = UmgeniWaterSource()
    tenders = source.parse_html(MOCK_UMGENI_WATER_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "UW/2025/CE/22"
    assert "Dam Wall Rehabilitation" in t1.title
    assert t1.required_cidb_class == "CE"
    assert t1.required_cidb_level == 5
    t2 = tenders[1]
    assert t2.tender_id == "UW/2025/EE/07"
    assert t2.required_cidb_class == "EE"
    assert t2.required_cidb_level == 3

def test_umgeni_water_fetch_uses_fallback_on_empty_or_error():
    source = UmgeniWaterSource()
    tenders = source.fetch(html_content="<html><body>No</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "UW/2025/EE/07" for t in tenders)
