"""Tests for the Musina (alt) tender source plug-in."""
import pytest


def test_musina_lm_alt_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.musina_lm_alt_tenders import MusinaLmAltSource
    src = MusinaLmAltSource()
    assert src.source_id == "musina_lm_alt_tenders"
    assert src.live is False


def test_musina_lm_alt_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.musina_lm_alt_tenders import MusinaLmAltSource, MOCK_HTML
    src = MusinaLmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_musina_lm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.musina_lm_alt_tenders import MusinaLmAltSource
    src = MusinaLmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
