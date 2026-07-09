"""Tests for the Chemical Industries Education and Training Authority (CHIETA) tender source plug-in."""
import pytest


def test_chieta_source_initialization():
    from tender_getter.sources.setas.chieta import ChietaSource
    src = ChietaSource()
    assert src.source_id == "chieta"
    assert isinstance(src.live, bool)


def test_chieta_parse_mock_html():
    from tender_getter.sources.setas.chieta import ChietaSource, MOCK_HTML
    src = ChietaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_chieta_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.chieta import ChietaSource
    src = ChietaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
