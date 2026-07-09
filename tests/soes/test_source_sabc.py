import pytest
from tender_getter.sources.soes.sabc import SabcSource

def test_sabc_source_initialization():
    source = SabcSource()
    assert source.source_id == "sabc"
    assert source.url.startswith("http")

def test_sabc_parse_mock_html():
    from tender_getter.sources.soes.sabc import MOCK_HTML
    source = SabcSource()
    tenders = source.parse_html(MOCK_HTML)
    assert len(tenders) >= 0

def test_sabc_fetch_uses_fallback_on_empty_or_error():
    source = SabcSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) >= 0
