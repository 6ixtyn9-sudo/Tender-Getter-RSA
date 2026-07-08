import pytest
from tender_getter.sources.soes.sentech import SentechSource, MOCK_SENTECH_HTML

def test_sentech_source_initialization():
    source = SentechSource()
    assert source.source_id == "sentech_tenders"
    assert source.url.startswith("http")

def test_sentech_parse_mock_html():
    source = SentechSource()
    tenders = source.parse_html(MOCK_SENTECH_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "SENTECH/2025/RF/09"
    assert "Signal Tower Maintenance" in t1.title
    assert t1.required_cidb_class == "EE"
    assert t1.required_cidb_level == 3
    assert t1.location_target in ["National", "National", "Gauteng", "Western Cape", "Mpumalanga", "Northern Cape"]
    assert t1.closing_date.year == 2026
    t2 = tenders[1]
    assert t2.tender_id == "SENTECH/2025/ICT/15"
    assert t2.required_cidb_class is None

def test_sentech_fetch_uses_fallback_on_empty_or_error():
    source = SentechSource()
    tenders = source.fetch(html_content="<html><body>No tenders</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "SENTECH/2025/ICT/15" for t in tenders)
