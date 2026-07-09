"""Tests for the Mining Qualifications Authority (already in setas/) tender source plug-in."""
import pytest


def test_bosasa_source_initialization():
    from tender_getter.sources.setas.bosasa import BosasaSource
    src = BosasaSource()
    assert src.source_id == "bosasa"
    assert src.live is True


def test_bosasa_parse_mock_html():
    from tender_getter.sources.setas.bosasa import BosasaSource, MOCK_HTML
    src = BosasaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_bosasa_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.bosasa import BosasaSource
    src = BosasaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
