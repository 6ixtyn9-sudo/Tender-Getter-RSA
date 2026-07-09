"""Tests for the Limpopo Parks Board tender source plug-in."""
import pytest


def test_lp_parks_source_initialization():
    from tender_getter.sources.research.lp_parks import LpParksSource
    src = LpParksSource()
    assert src.source_id == "lp_parks"
    assert isinstance(src.live, bool)


def test_lp_parks_parse_mock_html():
    from tender_getter.sources.research.lp_parks import LpParksSource, MOCK_HTML
    src = LpParksSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lp_parks_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.lp_parks import LpParksSource
    src = LpParksSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
