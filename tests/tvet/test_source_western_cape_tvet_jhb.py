"""Tests for the Western Cape TVET (JHB campus) tender source plug-in."""
import pytest


def test_western_cape_tvet_jhb_source_initialization():
    from tender_getter.sources.tvet.western_cape_tvet_jhb import WesternCapeTvetJhbSource
    src = WesternCapeTvetJhbSource()
    assert src.source_id == "western_cape_tvet_jhb"
    assert isinstance(src.live, bool)


def test_western_cape_tvet_jhb_parse_mock_html():
    from tender_getter.sources.tvet.western_cape_tvet_jhb import WesternCapeTvetJhbSource, MOCK_HTML
    src = WesternCapeTvetJhbSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_western_cape_tvet_jhb_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.western_cape_tvet_jhb import WesternCapeTvetJhbSource
    src = WesternCapeTvetJhbSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
