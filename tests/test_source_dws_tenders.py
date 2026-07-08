"""Tests for the Department of Water and Sanitation tender source plug-in."""
import pytest


def test_dws_tenders_source_initialization():
    from tender_getter.sources.research_extra.dws_tenders import DwsSource
    src = DwsSource()
    assert src.source_id == "dws_tenders"
    assert src.live is True


def test_dws_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.dws_tenders import DwsSource, MOCK_HTML
    src = DwsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dws_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.dws_tenders import DwsSource
    src = DwsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
