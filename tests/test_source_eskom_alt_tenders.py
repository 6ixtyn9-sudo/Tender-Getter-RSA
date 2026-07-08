"""Tests for the Eskom (alt) tender source plug-in."""
import pytest


def test_eskom_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.eskom_alt_tenders import EskomAltSource
    src = EskomAltSource()
    assert src.source_id == "eskom_alt_tenders"
    assert src.live is True


def test_eskom_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.eskom_alt_tenders import EskomAltSource, MOCK_HTML
    src = EskomAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_eskom_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.eskom_alt_tenders import EskomAltSource
    src = EskomAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
