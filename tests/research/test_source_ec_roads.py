"""Tests for the Eastern Cape Roads Agency tender source plug-in."""
import pytest


def test_ec_roads_source_initialization():
    from tender_getter.sources.research.ec_roads import EcRoadsSource
    src = EcRoadsSource()
    assert src.source_id == "ec_roads"
    assert isinstance(src.live, bool)


def test_ec_roads_parse_mock_html():
    from tender_getter.sources.research.ec_roads import EcRoadsSource, MOCK_HTML
    src = EcRoadsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ec_roads_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.ec_roads import EcRoadsSource
    src = EcRoadsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
