"""Tests for the CapeNature (Western Cape) tender source plug-in."""
import pytest


def test_capenature_source_initialization():
    from tender_getter.sources.research.capenature import CapenatureSource
    src = CapenatureSource()
    assert src.source_id == "capenature"
    assert src.live is True


def test_capenature_parse_mock_html():
    from tender_getter.sources.research.capenature import CapenatureSource, MOCK_HTML
    src = CapenatureSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_capenature_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.capenature import CapenatureSource
    src = CapenatureSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
