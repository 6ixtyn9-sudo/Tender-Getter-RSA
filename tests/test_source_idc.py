import pytest
from tender_getter.sources.dfi.idc import IDCSource, MOCK_IDC_HTML

def test_idc_source_initialization():
    source = IDCSource()
    assert source.source_id == "idc"
    assert source.url.startswith("http")

def test_idc_parse_mock_html():
    source = IDCSource()
    tenders = source.parse_html(MOCK_IDC_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "IDC/2025/SME/09"
    assert "SMME Development" in t1.title

def test_idc_fetch_uses_fallback_on_empty_or_error():
    source = IDCSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "IDC/2025/FIN/04" for t in tenders)
