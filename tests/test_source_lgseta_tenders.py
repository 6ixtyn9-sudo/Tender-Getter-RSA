"""Tests for the Local Government Sector Education and Training Authority (LGSETA) tender source plug-in."""
import pytest


def test_lgseta_tenders_source_initialization():
    from tender_getter.sources.setas.lgseta_tenders import LgsetaSource
    src = LgsetaSource()
    assert src.source_id == "lgseta_tenders"
    assert src.live is True


def test_lgseta_tenders_parse_mock_html():
    from tender_getter.sources.setas.lgseta_tenders import LgsetaSource, MOCK_HTML
    src = LgsetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lgseta_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.lgseta_tenders import LgsetaSource
    src = LgsetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
