"""Tests for the Mpumalanga Parks Board (MTPA) tender source plug-in."""
import pytest


def test_mp_parks_source_initialization():
    from tender_getter.sources.research.mp_parks import MpParksSource
    src = MpParksSource()
    assert src.source_id == "mp_parks"
    assert src.live is False


def test_mp_parks_parse_mock_html():
    from tender_getter.sources.research.mp_parks import MpParksSource, MOCK_HTML
    src = MpParksSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mp_parks_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.mp_parks import MpParksSource
    src = MpParksSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
