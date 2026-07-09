import pytest
from tender_getter.sources.dfi.seda import SEDASource, MOCK_SEDA_HTML

def test_seda_source_initialization():
    source = SEDASource()
    assert source.source_id == "seda"
    assert source.url.startswith("http")

def test_seda_parse_mock_html():
    source = SEDASource()
    tenders = source.parse_html(MOCK_SEDA_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "SEDA/2025/TRAIN/15"
    assert "Entrepreneurship Training" in t1.title

def test_seda_fetch_uses_fallback_on_empty_or_error():
    source = SEDASource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "SEDA/2025/ICT/06" for t in tenders)
