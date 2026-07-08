"""Tests for the KZN Roads (DOT legacy) tender source plug-in."""
import pytest


def test_kzn_roads_source_initialization():
    from tender_getter.sources.research.kzn_roads import KznRoadsSource
    src = KznRoadsSource()
    assert src.source_id == "kzn_roads"
    assert src.live is True


def test_kzn_roads_parse_mock_html():
    from tender_getter.sources.research.kzn_roads import KznRoadsSource, MOCK_HTML
    src = KznRoadsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kzn_roads_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.kzn_roads import KznRoadsSource
    src = KznRoadsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
