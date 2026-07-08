import pytest
from tender_getter.sources.dfi.sanparks import SANParksSource, MOCK_SANPARKS_HTML

def test_sanparks_source_initialization():
    source = SANParksSource()
    assert source.source_id == "sanparks_tenders"
    assert source.url.startswith("http")

def test_sanparks_parse_mock_html():
    source = SANParksSource()
    tenders = source.parse_html(MOCK_SANPARKS_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "SANPARKS/2025/CE/11"
    assert "Game Reserve Fencing" in t1.title

def test_sanparks_fetch_uses_fallback_on_empty_or_error():
    source = SANParksSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "SANPARKS/2025/ROAD/04" for t in tenders)
