"""Tests for the Petroleum Agency SA (PASA) tender source plug-in."""
import pytest


def test_pasa_source_initialization():
    from tender_getter.sources.soes.pasa import PasaSource
    src = PasaSource()
    assert src.source_id == "pasa"
    assert src.live is True


def test_pasa_parse_mock_html():
    from tender_getter.sources.soes.pasa import PasaSource, MOCK_HTML
    src = PasaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_pasa_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.pasa import PasaSource
    src = PasaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
