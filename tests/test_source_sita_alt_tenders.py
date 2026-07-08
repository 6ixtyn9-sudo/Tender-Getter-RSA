"""Tests for the SITA (alt URL) tender source plug-in."""
import pytest


def test_sita_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.sita_alt_tenders import SitaAltSource
    src = SitaAltSource()
    assert src.source_id == "sita_alt_tenders"
    assert src.live is True


def test_sita_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.sita_alt_tenders import SitaAltSource, MOCK_HTML
    src = SitaAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sita_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.sita_alt_tenders import SitaAltSource
    src = SitaAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
