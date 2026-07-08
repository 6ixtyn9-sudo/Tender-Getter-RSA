"""Tests for the South African State Theatre tender source plug-in."""
import pytest


def test_state_theatre_source_initialization():
    from tender_getter.sources.research.state_theatre import StateTheatreSource
    src = StateTheatreSource()
    assert src.source_id == "state_theatre"
    assert src.live is True


def test_state_theatre_parse_mock_html():
    from tender_getter.sources.research.state_theatre import StateTheatreSource, MOCK_HTML
    src = StateTheatreSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_state_theatre_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.state_theatre import StateTheatreSource
    src = StateTheatreSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
