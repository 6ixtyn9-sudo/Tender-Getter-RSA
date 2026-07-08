"""Tests for the National Health Laboratory Service tender source plug-in."""
import pytest


def test_nhls_tenders_source_initialization():
    from tender_getter.sources.research_extra.nhls_tenders import NhlsSource
    src = NhlsSource()
    assert src.source_id == "nhls_tenders"
    assert src.live is True


def test_nhls_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.nhls_tenders import NhlsSource, MOCK_HTML
    src = NhlsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nhls_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.nhls_tenders import NhlsSource
    src = NhlsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
