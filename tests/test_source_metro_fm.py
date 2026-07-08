"""Tests for the Metro FM tender source plug-in."""
import pytest


def test_metro_fm_source_initialization():
    from tender_getter.sources.metros.metro_fm import MetroFmSource
    src = MetroFmSource()
    assert src.source_id == "metro_fm"
    assert src.live is False


def test_metro_fm_parse_mock_html():
    from tender_getter.sources.metros.metro_fm import MetroFmSource, MOCK_HTML
    src = MetroFmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_metro_fm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.metros.metro_fm import MetroFmSource
    src = MetroFmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
