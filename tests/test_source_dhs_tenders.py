"""Tests for the Department of Human Settlements tender source plug-in."""
import pytest


def test_dhs_tenders_source_initialization():
    from tender_getter.sources.research_extra.dhs_tenders import DhsSource
    src = DhsSource()
    assert src.source_id == "dhs_tenders"
    assert src.live is True


def test_dhs_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.dhs_tenders import DhsSource, MOCK_HTML
    src = DhsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dhs_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.dhs_tenders import DhsSource
    src = DhsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
