"""Tests for the Mahlangeni LM tender source plug-in."""
import pytest


def test_mahlangeni_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.mahlangeni_lm_tenders import MahlangeniLmSource
    src = MahlangeniLmSource()
    assert src.source_id == "mahlangeni_lm_tenders"
    assert src.live is False


def test_mahlangeni_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.mahlangeni_lm_tenders import MahlangeniLmSource, MOCK_HTML
    src = MahlangeniLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mahlangeni_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.mahlangeni_lm_tenders import MahlangeniLmSource
    src = MahlangeniLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
