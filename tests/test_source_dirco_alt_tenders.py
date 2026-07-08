"""Tests for the DIRCO (alt) tender source plug-in."""
import pytest


def test_dirco_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.dirco_alt_tenders import DircoAltSource
    src = DircoAltSource()
    assert src.source_id == "dirco_alt_tenders"
    assert src.live is True


def test_dirco_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.dirco_alt_tenders import DircoAltSource, MOCK_HTML
    src = DircoAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dirco_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.dirco_alt_tenders import DircoAltSource
    src = DircoAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
