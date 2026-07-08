"""Tests for the SANParks (alt) tender source plug-in."""
import pytest


def test_sanparks_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.sanparks_alt_tenders import SanparksAltSource
    src = SanparksAltSource()
    assert src.source_id == "sanparks_alt_tenders"
    assert src.live is True


def test_sanparks_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.sanparks_alt_tenders import SanparksAltSource, MOCK_HTML
    src = SanparksAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sanparks_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.sanparks_alt_tenders import SanparksAltSource
    src = SanparksAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
