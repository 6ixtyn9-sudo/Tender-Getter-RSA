import pytest
from tender_getter.sources.provincial_depts.kzn_human_settlements import KZNHumanSettlementsSource, MOCK_KZN_HUMAN_SETTLEMENTS_HTML
def test_kzn_human_settlements_source_initialization():
    source = KZNHumanSettlementsSource()
    assert source.source_id == "kzn_human_settlements_tenders"
    assert source.url.startswith("http")
def test_kzn_human_settlements_parse_mock_html():
    source = KZNHumanSettlementsSource()
    tenders = source.parse_html(MOCK_KZN_HUMAN_SETTLEMENTS_HTML)
    assert len(tenders) == 3
def test_kzn_human_settlements_fetch_uses_fallback_on_empty_or_error():
    source = KZNHumanSettlementsSource()
    tenders = source.fetch(html_content="<html></html>")
    assert len(tenders) == 3
