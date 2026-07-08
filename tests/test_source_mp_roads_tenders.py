"""Tests for the Mpumalanga Roads Agency tender source plug-in."""
import pytest


def test_mp_roads_tenders_source_initialization():
    from tender_getter.sources.research_extra.mp_roads_tenders import MpRoadsSource
    src = MpRoadsSource()
    assert src.source_id == "mp_roads_tenders"
    assert src.live is False


def test_mp_roads_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.mp_roads_tenders import MpRoadsSource, MOCK_HTML
    src = MpRoadsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mp_roads_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.mp_roads_tenders import MpRoadsSource
    src = MpRoadsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
