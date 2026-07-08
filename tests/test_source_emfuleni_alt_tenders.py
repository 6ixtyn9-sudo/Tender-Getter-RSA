"""Tests for the Emfuleni (alt) tender source plug-in."""
import pytest


def test_emfuleni_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.emfuleni_alt_tenders import EmfuleniAltSource
    src = EmfuleniAltSource()
    assert src.source_id == "emfuleni_alt_tenders"
    assert src.live is True


def test_emfuleni_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.emfuleni_alt_tenders import EmfuleniAltSource, MOCK_HTML
    src = EmfuleniAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_emfuleni_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.emfuleni_alt_tenders import EmfuleniAltSource
    src = EmfuleniAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
