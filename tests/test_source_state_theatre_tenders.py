"""Tests for the South African State Theatre tender source plug-in."""
import pytest


def test_state_theatre_tenders_source_initialization():
    from tender_getter.sources.research_extra.state_theatre_tenders import StateTheatreSource
    src = StateTheatreSource()
    assert src.source_id == "state_theatre_tenders"
    assert src.live is True


def test_state_theatre_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.state_theatre_tenders import StateTheatreSource, MOCK_HTML
    src = StateTheatreSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_state_theatre_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.state_theatre_tenders import StateTheatreSource
    src = StateTheatreSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
