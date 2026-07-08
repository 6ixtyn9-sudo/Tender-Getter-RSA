"""Tests for the PRASA (alt) tender source plug-in."""
import pytest


def test_prasa_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.prasa_alt_tenders import PrasaAltSource
    src = PrasaAltSource()
    assert src.source_id == "prasa_alt_tenders"
    assert src.live is True


def test_prasa_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.prasa_alt_tenders import PrasaAltSource, MOCK_HTML
    src = PrasaAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_prasa_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.prasa_alt_tenders import PrasaAltSource
    src = PrasaAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
