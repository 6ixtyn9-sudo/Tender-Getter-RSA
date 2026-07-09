"""Tests for the Local Government Sector Education and Training Authority (LGSETA) tender source plug-in."""
import pytest


def test_lgseta_source_initialization():
    from tender_getter.sources.setas.lgseta import LgsetaSource
    src = LgsetaSource()
    assert src.source_id == "lgseta"
    assert isinstance(src.live, bool)


def test_lgseta_parse_mock_html():
    from tender_getter.sources.setas.lgseta import LgsetaSource, MOCK_HTML
    src = LgsetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lgseta_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.lgseta import LgsetaSource
    src = LgsetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
