"""Tests for the Musina Local Municipality tender source plug-in."""
import pytest


def test_musina_lm_source_initialization():
    from tender_getter.sources.local_municipalities.musina_lm import MusinaLmSource
    src = MusinaLmSource()
    assert src.source_id == "musina_lm"
    assert src.live is True


def test_musina_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.musina_lm import MusinaLmSource, MOCK_HTML
    src = MusinaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_musina_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.musina_lm import MusinaLmSource
    src = MusinaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
