"""Tests for the North West Parks Board tender source plug-in."""
import pytest


def test_nw_parks_source_initialization():
    from tender_getter.sources.research.nw_parks import NwParksSource
    src = NwParksSource()
    assert src.source_id == "nw_parks"
    assert isinstance(src.live, bool)


def test_nw_parks_parse_mock_html():
    from tender_getter.sources.research.nw_parks import NwParksSource, MOCK_HTML
    src = NwParksSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nw_parks_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nw_parks import NwParksSource
    src = NwParksSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
