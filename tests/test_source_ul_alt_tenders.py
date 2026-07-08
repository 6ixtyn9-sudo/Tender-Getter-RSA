"""Tests for the UL (alt) tender source plug-in."""
import pytest


def test_ul_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.ul_alt_tenders import UlAltSource
    src = UlAltSource()
    assert src.source_id == "ul_alt_tenders"
    assert src.live is True


def test_ul_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.ul_alt_tenders import UlAltSource, MOCK_HTML
    src = UlAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ul_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.ul_alt_tenders import UlAltSource
    src = UlAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
