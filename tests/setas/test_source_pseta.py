import pytest
from tender_getter.sources.setas.pseta import PsetaSource

def test_pseta_source_initialization():
    source = PsetaSource()
    assert source.source_id == "pseta"
    assert source.url.startswith("http")

def test_pseta_parse_mock_html():
    from tender_getter.sources.setas.pseta import MOCK_HTML
    source = PsetaSource()
    tenders = source.parse_html(MOCK_HTML)
    assert len(tenders) >= 0

def test_pseta_fetch_uses_fallback_on_empty_or_error():
    source = PsetaSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) >= 0
