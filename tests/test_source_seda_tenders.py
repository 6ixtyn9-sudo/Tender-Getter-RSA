"""Tests for the Small Enterprise Development Agency tender source plug-in."""
import pytest


def test_seda_tenders_source_initialization():
    from tender_getter.sources.research_extra.seda_tenders import SedaSource
    src = SedaSource()
    assert src.source_id == "seda_tenders"
    assert src.live is True


def test_seda_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.seda_tenders import SedaSource, MOCK_HTML
    src = SedaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_seda_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.seda_tenders import SedaSource
    src = SedaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
