import pytest
from tender_getter.sources.districts.ehlanzeni import EhlanzeniSource, MOCK_EHLANZENI_HTML
def test_ehlanzeni_source_initialization():
    source = EhlanzeniSource()
    assert source.source_id == "ehlanzeni_tenders"
    assert source.url.startswith("http")
def test_ehlanzeni_parse_mock_html():
    source = EhlanzeniSource()
    tenders = source.parse_html(MOCK_EHLANZENI_HTML)
    assert len(tenders) == 3
def test_ehlanzeni_fetch_uses_fallback_on_empty_or_error():
    source = EhlanzeniSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
