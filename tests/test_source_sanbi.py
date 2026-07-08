"""Tests for the South African National Biodiversity Institute (SANBI) tender source plug-in."""
import pytest


def test_sanbi_source_initialization():
    from tender_getter.sources.research.sanbi import SanbiSource
    src = SanbiSource()
    assert src.source_id == "sanbi"
    assert src.live is True


def test_sanbi_parse_mock_html():
    from tender_getter.sources.research.sanbi import SanbiSource, MOCK_HTML
    src = SanbiSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sanbi_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.sanbi import SanbiSource
    src = SanbiSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
