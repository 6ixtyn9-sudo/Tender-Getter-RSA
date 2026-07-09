import pytest
from tender_getter.sources.dfi.samsa import SAMSASource, MOCK_SAMSA_HTML

def test_samsa_source_initialization():
    source = SAMSASource()
    assert source.source_id == "samsa"
    assert source.url.startswith("http")

def test_samsa_parse_mock_html():
    source = SAMSASource()
    tenders = source.parse_html(MOCK_SAMSA_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "SAMSA/2025/ENV/05"
    assert "Ocean Pollution" in t1.title

def test_samsa_fetch_uses_fallback_on_empty_or_error():
    source = SAMSASource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "SAMSA/2025/INSP/02" for t in tenders)
