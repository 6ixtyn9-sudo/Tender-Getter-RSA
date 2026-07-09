import pytest
from tender_getter.sources.dfi.sefa import SefaSource, MOCK_SEFA_HTML

def test_sefa_source_initialization():
    source = SefaSource()
    assert source.source_id == "sefa"
    assert source.url.startswith("http")

def test_sefa_parse_mock_html():
    source = SefaSource()
    tenders = source.parse_html(MOCK_SEFA_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "sefa/2025/ICT/08"
    assert "Loan Management" in t1.title

def test_sefa_fetch_uses_fallback_on_empty_or_error():
    source = SefaSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "sefa/2025/FIN/02" for t in tenders)
