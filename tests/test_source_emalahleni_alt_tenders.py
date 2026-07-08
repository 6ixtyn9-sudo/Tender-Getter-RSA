"""Tests for the Emalahleni (alt) tender source plug-in."""
import pytest


def test_emalahleni_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.emalahleni_alt_tenders import EmalahleniAltSource
    src = EmalahleniAltSource()
    assert src.source_id == "emalahleni_alt_tenders"
    assert src.live is True


def test_emalahleni_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.emalahleni_alt_tenders import EmalahleniAltSource, MOCK_HTML
    src = EmalahleniAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_emalahleni_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.emalahleni_alt_tenders import EmalahleniAltSource
    src = EmalahleniAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
