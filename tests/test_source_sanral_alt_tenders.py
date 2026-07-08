"""Tests for the SANRAL (alt) tender source plug-in."""
import pytest


def test_sanral_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.sanral_alt_tenders import SanralAltSource
    src = SanralAltSource()
    assert src.source_id == "sanral_alt_tenders"
    assert src.live is True


def test_sanral_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.sanral_alt_tenders import SanralAltSource, MOCK_HTML
    src = SanralAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sanral_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.sanral_alt_tenders import SanralAltSource
    src = SanralAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
