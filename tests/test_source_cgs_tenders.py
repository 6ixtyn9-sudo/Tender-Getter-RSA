"""Tests for the Council for Geoscience (already in research/) tender source plug-in."""
import pytest


def test_cgs_tenders_source_initialization():
    from tender_getter.sources.research_extra.cgs_tenders import CgsSource
    src = CgsSource()
    assert src.source_id == "cgs_tenders"
    assert src.live is True


def test_cgs_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.cgs_tenders import CgsSource, MOCK_HTML
    src = CgsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_cgs_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.cgs_tenders import CgsSource
    src = CgsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
