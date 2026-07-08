import pytest
from tender_getter.sources.water.tcta import TCTASource, MOCK_TCTA_HTML

def test_tcta_source_initialization():
    source = TCTASource()
    assert source.source_id == "tcta_tenders"
    assert source.url.startswith("http")

def test_tcta_parse_mock_html():
    source = TCTASource()
    tenders = source.parse_html(MOCK_TCTA_HTML)
    assert len(tenders) == 3
    t1 = tenders[0]
    assert t1.tender_id == "TCTA/2025/CE/19"
    assert "Tunnel Engineering" in t1.title
    assert t1.required_cidb_class == "CE"
    assert t1.required_cidb_level == 7
    t2 = tenders[1]
    assert t2.tender_id == "TCTA/2025/FIN/04"
    assert t2.required_cidb_class is None

def test_tcta_fetch_uses_fallback_on_empty_or_error():
    source = TCTASource()
    tenders = source.fetch(html_content="<html><body>No</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "TCTA/2025/FIN/04" for t in tenders)
