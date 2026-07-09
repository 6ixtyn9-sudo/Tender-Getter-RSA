"""Tests for the Council for Geoscience (already in research/) tender source plug-in."""
import pytest


def test_cgs_source_initialization():
    from tender_getter.sources.research.cgs import CgsSource
    src = CgsSource()
    assert src.source_id == "cgs"
    assert isinstance(src.live, bool)


def test_cgs_parse_mock_html():
    from tender_getter.sources.research.cgs import CgsSource, MOCK_HTML
    src = CgsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_cgs_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.cgs import CgsSource
    src = CgsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
