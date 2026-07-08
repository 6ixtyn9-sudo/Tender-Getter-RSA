import pytest
from datetime import datetime, timezone
from tender_getter.sources.metros.ethekwini import EthekwiniSource, MOCK_ETHEKWINI_HTML

def test_ethekwini_source_initialization():
    source = EthekwiniSource()
    assert source.source_id == "ethekwini"
    assert source.url.startswith("http")

def test_ethekwini_parse_mock_html():
    source = EthekwiniSource()
    tenders = source.parse_html(MOCK_ETHEKWINI_HTML)
    
    assert len(tenders) == 3
    
    # Verify first tender
    t1 = tenders[0]
    assert t1.tender_id == "ETH/EE042/25-26"
    assert "Port Electrical Reticulation" in t1.title
    assert t1.required_cidb_class == "EE"
    assert t1.required_cidb_level == 5
    assert t1.location_target == "KwaZulu-Natal"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 9
    assert t1.closing_date.day == 5

    # Verify second tender
    t2 = tenders[1]
    assert t2.tender_id == "ETH/CE118/25-26"
    assert t2.required_cidb_class == "CE"
    assert t2.required_cidb_level == 6
    assert t2.location_target == "KwaZulu-Natal"

def test_ethekwini_fetch_uses_fallback_on_empty_or_error():
    source = EthekwiniSource()
    tenders = source.fetch(html_content="<html><body>No tenders or tables here!</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "ETH/CE118/25-26" for t in tenders)
