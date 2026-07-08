"""Tests for the Western Cape TVET (JHB campus) tender source plug-in."""
import pytest


def test_western_cape_tvet_jhb_tenders_source_initialization():
    from tender_getter.sources.tvet.western_cape_tvet_jhb_tenders import WesternCapeTvetJhbSource
    src = WesternCapeTvetJhbSource()
    assert src.source_id == "western_cape_tvet_jhb_tenders"
    assert src.live is True


def test_western_cape_tvet_jhb_tenders_parse_mock_html():
    from tender_getter.sources.tvet.western_cape_tvet_jhb_tenders import WesternCapeTvetJhbSource, MOCK_HTML
    src = WesternCapeTvetJhbSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_western_cape_tvet_jhb_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.western_cape_tvet_jhb_tenders import WesternCapeTvetJhbSource
    src = WesternCapeTvetJhbSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
