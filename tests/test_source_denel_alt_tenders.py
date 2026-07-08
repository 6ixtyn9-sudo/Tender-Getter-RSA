"""Tests for the Denel (alt) tender source plug-in."""
import pytest


def test_denel_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.denel_alt_tenders import DenelAltSource
    src = DenelAltSource()
    assert src.source_id == "denel_alt_tenders"
    assert src.live is False


def test_denel_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.denel_alt_tenders import DenelAltSource, MOCK_HTML
    src = DenelAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_denel_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.denel_alt_tenders import DenelAltSource
    src = DenelAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
