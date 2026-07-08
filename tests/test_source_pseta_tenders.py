"""Tests for the Public Service Sector Education and Training Authority (PSETA) tender source plug-in."""
import pytest


def test_pseta_tenders_source_initialization():
    from tender_getter.sources.setas.pseta_tenders import PsetaSource
    src = PsetaSource()
    assert src.source_id == "pseta_tenders"
    assert src.live is True


def test_pseta_tenders_parse_mock_html():
    from tender_getter.sources.setas.pseta_tenders import PsetaSource, MOCK_HTML
    src = PsetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_pseta_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.pseta_tenders import PsetaSource
    src = PsetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
