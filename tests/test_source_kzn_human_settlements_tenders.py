"""Tests for the KwaZulu-Natal Department of Human Settlements tender source plug-in."""
import pytest


def test_kzn_human_settlements_tenders_source_initialization():
    from tender_getter.sources.research_extra.kzn_human_settlements_tenders import KznHumanSettlementsSource
    src = KznHumanSettlementsSource()
    assert src.source_id == "kzn_human_settlements_tenders"
    assert src.live is True


def test_kzn_human_settlements_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.kzn_human_settlements_tenders import KznHumanSettlementsSource, MOCK_HTML
    src = KznHumanSettlementsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kzn_human_settlements_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.kzn_human_settlements_tenders import KznHumanSettlementsSource
    src = KznHumanSettlementsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
