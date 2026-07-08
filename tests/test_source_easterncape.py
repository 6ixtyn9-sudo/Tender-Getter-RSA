import pytest
from datetime import datetime, timezone
from tender_getter.sources.provincial.easterncape import EasternCapeSource, MOCK_EASTERNCAPE_HTML

def test_easterncape_source_initialization():
    source = EasternCapeSource()
    assert source.source_id == "easterncape"
    assert source.url.startswith("http")

def test_easterncape_parse_mock_html():
    source = EasternCapeSource()
    tenders = source.parse_html(MOCK_EASTERNCAPE_HTML)
    
    assert len(tenders) == 3
    
    t1 = tenders[0]
    assert t1.tender_id == "ECPT/EE/2025/11"
    assert "School Electrification" in t1.title
    assert t1.required_cidb_class == "EE"
    assert t1.required_cidb_level == 3
    assert t1.location_target == "Eastern Cape"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 9
    assert t1.closing_date.day == 6

    t2 = tenders[1]
    assert t2.tender_id == "ECPT/CE/2025/22"
    assert t2.required_cidb_class == "CE"
    assert t2.required_cidb_level == 5
    assert t2.location_target == "Eastern Cape"

def test_easterncape_fetch_uses_fallback_on_empty_or_error():
    source = EasternCapeSource()
    tenders = source.fetch(html_content="<html><body>No tenders</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "ECPT/CE/2025/22" for t in tenders)
