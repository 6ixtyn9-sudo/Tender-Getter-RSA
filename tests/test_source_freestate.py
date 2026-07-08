import pytest
from datetime import datetime, timezone
from tender_getter.sources.provincial.freestate import FreeStateSource, MOCK_FREESTATE_HTML

def test_freestate_source_initialization():
    source = FreeStateSource()
    assert source.source_id == "freestate_tenders"
    assert source.url.startswith("http")

def test_freestate_parse_mock_html():
    source = FreeStateSource()
    tenders = source.parse_html(MOCK_FREESTATE_HTML)
    
    assert len(tenders) == 3
    
    t1 = tenders[0]
    assert t1.tender_id == "FSPT/CE/051/2025"
    assert "Bridge Repair" in t1.title
    assert t1.required_cidb_class == "CE"
    assert t1.required_cidb_level == 4
    assert t1.location_target == "Free State"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 9
    assert t1.closing_date.day == 9

    t2 = tenders[1]
    assert t2.tender_id == "FSPT/EE/033/2025"
    assert t2.required_cidb_class == "EE"
    assert t2.required_cidb_level == 3
    assert t2.location_target == "Free State"

def test_freestate_fetch_uses_fallback_on_empty_or_error():
    source = FreeStateSource()
    tenders = source.fetch(html_content="<html><body>No tenders</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "FSPT/EE/033/2025" for t in tenders)
