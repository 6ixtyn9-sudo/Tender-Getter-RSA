"""Tests for the Gauteng Parks tender source plug-in."""
import pytest


def test_gp_parks_tenders_source_initialization():
    from tender_getter.sources.research_extra.gp_parks_tenders import GpParksSource
    src = GpParksSource()
    assert src.source_id == "gp_parks_tenders"
    assert src.live is False


def test_gp_parks_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.gp_parks_tenders import GpParksSource, MOCK_HTML
    src = GpParksSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gp_parks_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.gp_parks_tenders import GpParksSource
    src = GpParksSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
