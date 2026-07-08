import pytest
from tender_getter.sources.dfi.raf import RAFSource, MOCK_RAF_HTML

def test_raf_source_initialization():
    source = RAFSource()
    assert source.source_id == "raf_tenders"
    assert source.url.startswith("http")

def test_raf_parse_mock_html():
    source = RAFSource()
    tenders = source.parse_html(MOCK_RAF_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "RAF/2025/LEGAL/19"
    assert "Legal Panel" in t1.title

def test_raf_fetch_uses_fallback_on_empty_or_error():
    source = RAFSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "RAF/2025/MED/07" for t in tenders)
