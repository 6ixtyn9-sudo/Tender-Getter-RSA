"""Tests for the North West Parks Board tender source plug-in."""
import pytest


def test_nw_parks_tenders_source_initialization():
    from tender_getter.sources.research_extra.nw_parks_tenders import NwParksSource
    src = NwParksSource()
    assert src.source_id == "nw_parks_tenders"
    assert src.live is False


def test_nw_parks_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.nw_parks_tenders import NwParksSource, MOCK_HTML
    src = NwParksSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nw_parks_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.nw_parks_tenders import NwParksSource
    src = NwParksSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
