import pytest
from tender_getter.sources.provincial_depts.gde import GDESource, MOCK_GDE_HTML
def test_gde_source_initialization():
    source = GDESource()
    assert source.source_id == "gde"
    assert source.url.startswith("http")
def test_gde_parse_mock_html():
    source = GDESource()
    tenders = source.parse_html(MOCK_GDE_HTML)
    assert len(tenders) == 3
def test_gde_fetch_uses_fallback_on_empty_or_error():
    source = GDESource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
