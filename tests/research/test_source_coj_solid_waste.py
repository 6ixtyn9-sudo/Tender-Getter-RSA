"""Tests for the CoJ Solid Waste tender source plug-in."""
import pytest


def test_coj_solid_waste_source_initialization():
    from tender_getter.sources.research.coj_solid_waste import CojSolidWasteSource
    src = CojSolidWasteSource()
    assert src.source_id == "coj_solid_waste"
    assert isinstance(src.live, bool)


def test_coj_solid_waste_parse_mock_html():
    from tender_getter.sources.research.coj_solid_waste import CojSolidWasteSource, MOCK_HTML
    src = CojSolidWasteSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_coj_solid_waste_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.coj_solid_waste import CojSolidWasteSource
    src = CojSolidWasteSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
