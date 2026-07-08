import pytest
from tender_getter.sources.dfi.dbsa import DBSASource, MOCK_DBSA_HTML

def test_dbsa_source_initialization():
    source = DBSASource()
    assert source.source_id == "dbsa"
    assert source.url.startswith("http")

def test_dbsa_parse_mock_html():
    source = DBSASource()
    tenders = source.parse_html(MOCK_DBSA_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "DBSA/2025/CONS/14"
    assert "Municipal Infrastructure" in t1.title

def test_dbsa_fetch_uses_fallback_on_empty_or_error():
    source = DBSASource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "DBSA/2025/ICT/06" for t in tenders)
