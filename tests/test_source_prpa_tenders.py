"""Tests for the Pension Funds Adjudicator (alt) tender source plug-in."""
import pytest


def test_prpa_tenders_source_initialization():
    from tender_getter.sources.research_extra.prpa_tenders import PrpaSource
    src = PrpaSource()
    assert src.source_id == "prpa_tenders"
    assert src.live is False


def test_prpa_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.prpa_tenders import PrpaSource, MOCK_HTML
    src = PrpaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_prpa_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.prpa_tenders import PrpaSource
    src = PrpaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
