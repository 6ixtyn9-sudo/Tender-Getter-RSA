import pytest
from tender_getter.sources.national_depts.presidency import PresidencySource, MOCK_PRESIDENCY_HTML
def test_presidency_source_initialization():
    source = PresidencySource()
    assert source.source_id == "presidency"
    assert source.url.startswith("http")
def test_presidency_parse_mock_html():
    source = PresidencySource()
    tenders = source.parse_html(MOCK_PRESIDENCY_HTML)
    assert len(tenders) == 3
def test_presidency_fetch_uses_fallback_on_empty_or_error():
    source = PresidencySource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
