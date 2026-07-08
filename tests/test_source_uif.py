import pytest
from tender_getter.sources.dfi.uif import UIFSource, MOCK_UIF_HTML

def test_uif_source_initialization():
    source = UIFSource()
    assert source.source_id == "uif"
    assert source.url.startswith("http")

def test_uif_parse_mock_html():
    source = UIFSource()
    tenders = source.parse_html(MOCK_UIF_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "UIF/2025/ICT/14"
    assert "Fraud Prevention" in t1.title

def test_uif_fetch_uses_fallback_on_empty_or_error():
    source = UIFSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "UIF/2025/SOFT/05" for t in tenders)
