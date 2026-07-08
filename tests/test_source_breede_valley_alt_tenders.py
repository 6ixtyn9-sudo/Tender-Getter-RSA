"""Tests for the Breede Valley (alt) tender source plug-in."""
import pytest


def test_breede_valley_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.breede_valley_alt_tenders import BreedeValleyAltSource
    src = BreedeValleyAltSource()
    assert src.source_id == "breede_valley_alt_tenders"
    assert src.live is True


def test_breede_valley_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.breede_valley_alt_tenders import BreedeValleyAltSource, MOCK_HTML
    src = BreedeValleyAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_breede_valley_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.breede_valley_alt_tenders import BreedeValleyAltSource
    src = BreedeValleyAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
