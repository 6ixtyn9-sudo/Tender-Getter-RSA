"""Tests for the Eastern Cape Roads Agency tender source plug-in."""
import pytest


def test_ec_roads_tenders_source_initialization():
    from tender_getter.sources.research_extra.ec_roads_tenders import EcRoadsSource
    src = EcRoadsSource()
    assert src.source_id == "ec_roads_tenders"
    assert src.live is False


def test_ec_roads_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.ec_roads_tenders import EcRoadsSource, MOCK_HTML
    src = EcRoadsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ec_roads_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.ec_roads_tenders import EcRoadsSource
    src = EcRoadsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
