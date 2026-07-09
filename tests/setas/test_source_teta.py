"""Tests for the Transport Education Training Authority (TETA) tender source plug-in."""
import pytest


def test_teta_source_initialization():
    from tender_getter.sources.setas.teta import TetaSource
    src = TetaSource()
    assert src.source_id == "teta"
    assert isinstance(src.live, bool)


def test_teta_parse_mock_html():
    from tender_getter.sources.setas.teta import TetaSource, MOCK_HTML
    src = TetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_teta_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.teta import TetaSource
    src = TetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
