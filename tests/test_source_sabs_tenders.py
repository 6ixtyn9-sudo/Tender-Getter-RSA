"""Tests for the South African Bureau of Standards tender source plug-in."""
import pytest


def test_sabs_tenders_source_initialization():
    from tender_getter.sources.research_extra.sabs_tenders import SabsSource
    src = SabsSource()
    assert src.source_id == "sabs_tenders"
    assert src.live is True


def test_sabs_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.sabs_tenders import SabsSource, MOCK_HTML
    src = SabsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sabs_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.sabs_tenders import SabsSource
    src = SabsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
