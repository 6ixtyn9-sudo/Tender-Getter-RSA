"""Tests for the NYDA (alt URL) tender source plug-in."""
import pytest


def test_nyda_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.nyda_alt_tenders import NydaAltSource
    src = NydaAltSource()
    assert src.source_id == "nyda_alt_tenders"
    assert src.live is True


def test_nyda_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.nyda_alt_tenders import NydaAltSource, MOCK_HTML
    src = NydaAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nyda_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.nyda_alt_tenders import NydaAltSource
    src = NydaAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
