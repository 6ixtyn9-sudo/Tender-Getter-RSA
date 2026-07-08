"""Tests for the South African Tourism tender source plug-in."""
import pytest


def test_sat_tenders_source_initialization():
    from tender_getter.sources.schedule3a.sat_tenders import SatSource
    src = SatSource()
    assert src.source_id == "sat_tenders"
    assert src.live is True


def test_sat_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.sat_tenders import SatSource, MOCK_HTML
    src = SatSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sat_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.sat_tenders import SatSource
    src = SatSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
