"""Tests for the DTIC (alt URL) tender source plug-in."""
import pytest


def test_dtic_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.dtic_alt_tenders import DticAltSource
    src = DticAltSource()
    assert src.source_id == "dtic_alt_tenders"
    assert src.live is True


def test_dtic_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.dtic_alt_tenders import DticAltSource, MOCK_HTML
    src = DticAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dtic_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.dtic_alt_tenders import DticAltSource
    src = DticAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
