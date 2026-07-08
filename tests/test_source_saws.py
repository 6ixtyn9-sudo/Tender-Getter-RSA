"""Tests for the South African Weather Service (SAWS) tender source plug-in."""
import pytest


def test_saws_source_initialization():
    from tender_getter.sources.research.saws import SawsSource
    src = SawsSource()
    assert src.source_id == "saws"
    assert src.live is True


def test_saws_parse_mock_html():
    from tender_getter.sources.research.saws import SawsSource, MOCK_HTML
    src = SawsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_saws_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.saws import SawsSource
    src = SawsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
