import pytest
from tender_getter.sources.provincial_depts.limpopo_pwri import LimpopoPWRISource, MOCK_LIMPOPO_PWRI_HTML
def test_limpopo_pwri_source_initialization():
    source = LimpopoPWRISource()
    assert source.source_id == "limpopo_pwri"
    assert source.url.startswith("http")
def test_limpopo_pwri_parse_mock_html():
    source = LimpopoPWRISource()
    tenders = source.parse_html(MOCK_LIMPOPO_PWRI_HTML)
    assert len(tenders) == 3
def test_limpopo_pwri_fetch_uses_fallback_on_empty_or_error():
    source = LimpopoPWRISource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
