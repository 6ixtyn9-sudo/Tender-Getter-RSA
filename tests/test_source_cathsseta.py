"""Tests for the Culture, Arts, Tourism, Hospitality and Sport SETA (CATHSSETA) tender source plug-in."""
import pytest


def test_cathsseta_source_initialization():
    from tender_getter.sources.setas.cathsseta import CathssetaSource
    src = CathssetaSource()
    assert src.source_id == "cathsseta"
    assert src.live is True


def test_cathsseta_parse_mock_html():
    from tender_getter.sources.setas.cathsseta import CathssetaSource, MOCK_HTML
    src = CathssetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_cathsseta_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.cathsseta import CathssetaSource
    src = CathssetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
