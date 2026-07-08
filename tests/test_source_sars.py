import pytest
from tender_getter.sources.dfi.sars import SARSSource, MOCK_SARS_HTML

def test_sars_source_initialization():
    source = SARSSource()
    assert source.source_id == "sars_tenders"
    assert source.url.startswith("http")

def test_sars_parse_mock_html():
    source = SARSSource()
    tenders = source.parse_html(MOCK_SARS_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "SARS/2025/ICT/22"
    assert "Customs Inspection" in t1.title

def test_sars_fetch_uses_fallback_on_empty_or_error():
    source = SARSSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "SARS/2025/TECH/08" for t in tenders)
