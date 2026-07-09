"""Tests for the Swartland Municipality tender source plug-in."""
import pytest


def test_swartland_lm_source_initialization():
    from tender_getter.sources.local_municipalities.swartland_lm import SwartlandLmSource
    src = SwartlandLmSource()
    assert src.source_id == "swartland_lm"
    assert src.live is True


def test_swartland_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.swartland_lm import SwartlandLmSource, MOCK_HTML
    src = SwartlandLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_swartland_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.swartland_lm import SwartlandLmSource
    src = SwartlandLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
