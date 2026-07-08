"""Tests for the Land Bank (alt) tender source plug-in."""
import pytest


def test_landbank_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.landbank_alt_tenders import LandbankAltSource
    src = LandbankAltSource()
    assert src.source_id == "landbank_alt_tenders"
    assert src.live is True


def test_landbank_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.landbank_alt_tenders import LandbankAltSource, MOCK_HTML
    src = LandbankAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_landbank_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.landbank_alt_tenders import LandbankAltSource
    src = LandbankAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
