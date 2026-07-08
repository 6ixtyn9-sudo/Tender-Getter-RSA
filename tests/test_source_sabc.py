import pytest
from tender_getter.sources.soes.sabc import SABCSource, MOCK_SABC_HTML

def test_sabc_source_initialization():
    source = SABCSource()
    assert source.source_id == "sabc_tenders"
    assert source.url.startswith("http")

def test_sabc_parse_mock_html():
    source = SABCSource()
    tenders = source.parse_html(MOCK_SABC_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "SABC/TV/2025/14"
    assert "Studio Camera" in t1.title
    assert t1.required_cidb_class is None
    assert t1.location_target in ["Gauteng", "National", "Gauteng", "Western Cape", "Mpumalanga", "Northern Cape"]
    assert t1.closing_date.year == 2026
    t2 = tenders[1]
    assert t2.tender_id == "SABC/RADIO/2025/06"
    assert t2.required_cidb_class == "EE"
    assert t2.required_cidb_level == 3

def test_sabc_fetch_uses_fallback_on_empty_or_error():
    source = SABCSource()
    tenders = source.fetch(html_content="<html><body>No tenders</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "SABC/RADIO/2025/06" for t in tenders)
