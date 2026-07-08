"""Tests for the Mpumalanga Roads Agency tender source plug-in."""
import pytest


def test_mp_roads_source_initialization():
    from tender_getter.sources.research.mp_roads import MpRoadsSource
    src = MpRoadsSource()
    assert src.source_id == "mp_roads"
    assert src.live is False


def test_mp_roads_parse_mock_html():
    from tender_getter.sources.research.mp_roads import MpRoadsSource, MOCK_HTML
    src = MpRoadsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mp_roads_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.mp_roads import MpRoadsSource
    src = MpRoadsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
