"""Tests for the iLembe (DM legacy URL) tender source plug-in."""
import pytest


def test_iLembe_dm_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.iLembe_dm_alt_tenders import IlembeDmAltSource
    src = IlembeDmAltSource()
    assert src.source_id == "iLembe_dm_alt_tenders"
    assert src.live is False


def test_iLembe_dm_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.iLembe_dm_alt_tenders import IlembeDmAltSource, MOCK_HTML
    src = IlembeDmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_iLembe_dm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.iLembe_dm_alt_tenders import IlembeDmAltSource
    src = IlembeDmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
