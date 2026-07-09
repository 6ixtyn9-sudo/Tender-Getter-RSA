"""Tests for the Rail Safety Regulator (RSR) tender source plug-in."""
import pytest


def test_railersafety_source_initialization():
    from tender_getter.sources.research.railersafety import RailersafetySource
    src = RailersafetySource()
    assert src.source_id == "railersafety"
    assert src.live is True


def test_railersafety_parse_mock_html():
    from tender_getter.sources.research.railersafety import RailersafetySource, MOCK_HTML
    src = RailersafetySource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_railersafety_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.railersafety import RailersafetySource
    src = RailersafetySource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
