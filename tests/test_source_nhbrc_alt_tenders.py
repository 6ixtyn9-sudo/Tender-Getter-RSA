"""Tests for the NHBRC (alt) tender source plug-in."""
import pytest


def test_nhbrc_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.nhbrc_alt_tenders import NhbrcAltSource
    src = NhbrcAltSource()
    assert src.source_id == "nhbrc_alt_tenders"
    assert src.live is True


def test_nhbrc_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.nhbrc_alt_tenders import NhbrcAltSource, MOCK_HTML
    src = NhbrcAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nhbrc_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.nhbrc_alt_tenders import NhbrcAltSource
    src = NhbrcAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
