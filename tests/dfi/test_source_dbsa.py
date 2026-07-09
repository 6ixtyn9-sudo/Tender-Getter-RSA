import pytest
from tender_getter.sources.dfi.dbsa import DBSASource, MOCK_HTML

def test_dbsa_source_initialization():
    source = DBSASource()
    assert source.source_id == "dbsa"
    assert source.url.startswith("http")

def test_dbsa_parse_mock_html():
    source = DBSASource()
    tenders = source.parse_html(MOCK_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "DBSA/RFP 106/2026"
    assert "Procurement of a Legal" in t1.title

def test_dbsa_fetch_uses_fallback_on_empty_or_error():
    source = DBSASource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
