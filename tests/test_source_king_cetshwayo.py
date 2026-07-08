import pytest
from tender_getter.sources.districts.king_cetshwayo import KingCetshwayoSource, MOCK_KING_CETSHWAYO_HTML
def test_king_cetshwayo_source_initialization():
    source = KingCetshwayoSource()
    assert source.source_id == "king_cetshwayo_tenders"
    assert source.url.startswith("http")
def test_king_cetshwayo_parse_mock_html():
    source = KingCetshwayoSource()
    tenders = source.parse_html(MOCK_KING_CETSHWAYO_HTML)
    assert len(tenders) == 3
def test_king_cetshwayo_fetch_uses_fallback_on_empty_or_error():
    source = KingCetshwayoSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
