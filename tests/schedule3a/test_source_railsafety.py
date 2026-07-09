"""Tests for the Rail Safety Regulator (RSR) tender source plug-in."""
import pytest


def test_railsafety_source_initialization():
    from tender_getter.sources.schedule3a.railsafety import RailsafetySource
    src = RailsafetySource()
    assert src.source_id == "railsafety"
    assert isinstance(src.live, bool)


def test_railsafety_parse_mock_html():
    from tender_getter.sources.schedule3a.railsafety import RailsafetySource, MOCK_HTML
    src = RailsafetySource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_railsafety_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.railsafety import RailsafetySource
    src = RailsafetySource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
