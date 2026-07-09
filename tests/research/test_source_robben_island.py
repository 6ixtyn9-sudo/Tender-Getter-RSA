"""Tests for the Robben Island Museum tender source plug-in."""
import pytest


def test_robben_island_source_initialization():
    from tender_getter.sources.research.robben_island import RobbenIslandSource
    src = RobbenIslandSource()
    assert src.source_id == "robben_island"
    assert isinstance(src.live, bool)


def test_robben_island_parse_mock_html():
    from tender_getter.sources.research.robben_island import RobbenIslandSource, MOCK_HTML
    src = RobbenIslandSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_robben_island_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.robben_island import RobbenIslandSource
    src = RobbenIslandSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
