"""Tests for the Drakenstein (alt) tender source plug-in."""
import pytest


def test_drakenstein_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.drakenstein_alt_tenders import DrakensteinAltSource
    src = DrakensteinAltSource()
    assert src.source_id == "drakenstein_alt_tenders"
    assert src.live is True


def test_drakenstein_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.drakenstein_alt_tenders import DrakensteinAltSource, MOCK_HTML
    src = DrakensteinAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_drakenstein_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.drakenstein_alt_tenders import DrakensteinAltSource
    src = DrakensteinAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
