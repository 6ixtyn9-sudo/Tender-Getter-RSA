"""Tests for the South African National Blood Service (SANBS) tender source plug-in."""
import pytest


def test_sanbs_source_initialization():
    from tender_getter.sources.research.sanbs import SanbsSource
    src = SanbsSource()
    assert src.source_id == "sanbs"
    assert src.live is True


def test_sanbs_parse_mock_html():
    from tender_getter.sources.research.sanbs import SanbsSource, MOCK_HTML
    src = SanbsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sanbs_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.sanbs import SanbsSource
    src = SanbsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
