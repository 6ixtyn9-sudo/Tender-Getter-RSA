"""Tests for the Transport Education Training Authority (TETA) tender source plug-in."""
import pytest


def test_teta_tenders_source_initialization():
    from tender_getter.sources.setas.teta_tenders import TetaSource
    src = TetaSource()
    assert src.source_id == "teta_tenders"
    assert src.live is True


def test_teta_tenders_parse_mock_html():
    from tender_getter.sources.setas.teta_tenders import TetaSource, MOCK_HTML
    src = TetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_teta_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.teta_tenders import TetaSource
    src = TetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
