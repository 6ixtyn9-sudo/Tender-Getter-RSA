import pytest
from tender_getter.sources.soes.infraco import BroadbandInfracoSource, MOCK_INFRACO_HTML

def test_infraco_source_initialization():
    source = BroadbandInfracoSource()
    assert source.source_id == "infraco"
    assert source.url.startswith("http")

def test_infraco_parse_mock_html():
    source = BroadbandInfracoSource()
    tenders = source.parse_html(MOCK_INFRACO_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "INFRA/2025/FIBRE/21"
    assert "National Fibre Backhaul" in t1.title
    assert t1.required_cidb_class == "EE"
    assert t1.required_cidb_level == 5
    assert t1.location_target in ["National", "National", "Gauteng", "Western Cape", "Mpumalanga", "Northern Cape"]
    assert t1.closing_date.year == 2026
    t2 = tenders[1]
    assert t2.tender_id == "INFRA/2025/ICT/09"
    assert t2.required_cidb_class is None

def test_infraco_fetch_uses_fallback_on_empty_or_error():
    source = BroadbandInfracoSource()
    tenders = source.fetch(html_content="<html><body>No tenders</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "INFRA/2025/ICT/09" for t in tenders)
