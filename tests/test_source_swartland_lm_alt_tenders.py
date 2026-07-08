"""Tests for the Swartland (alt) tender source plug-in."""
import pytest


def test_swartland_lm_alt_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.swartland_lm_alt_tenders import SwartlandLmAltSource
    src = SwartlandLmAltSource()
    assert src.source_id == "swartland_lm_alt_tenders"
    assert src.live is True


def test_swartland_lm_alt_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.swartland_lm_alt_tenders import SwartlandLmAltSource, MOCK_HTML
    src = SwartlandLmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_swartland_lm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.swartland_lm_alt_tenders import SwartlandLmAltSource
    src = SwartlandLmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
