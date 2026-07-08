"""Tests for the Chemical Industries Education and Training Authority (CHIETA) tender source plug-in."""
import pytest


def test_chieta_tenders_source_initialization():
    from tender_getter.sources.setas.chieta_tenders import ChietaSource
    src = ChietaSource()
    assert src.source_id == "chieta_tenders"
    assert src.live is True


def test_chieta_tenders_parse_mock_html():
    from tender_getter.sources.setas.chieta_tenders import ChietaSource, MOCK_HTML
    src = ChietaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_chieta_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.chieta_tenders import ChietaSource
    src = ChietaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
