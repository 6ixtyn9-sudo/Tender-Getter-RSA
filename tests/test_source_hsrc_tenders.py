"""Tests for the Human Sciences Research Council tender source plug-in."""
import pytest


def test_hsrc_tenders_source_initialization():
    from tender_getter.sources.research_extra.hsrc_tenders import HsrcSource
    src = HsrcSource()
    assert src.source_id == "hsrc_tenders"
    assert src.live is True


def test_hsrc_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.hsrc_tenders import HsrcSource, MOCK_HTML
    src = HsrcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_hsrc_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.hsrc_tenders import HsrcSource
    src = HsrcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
