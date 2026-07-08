"""Tests for the Road Accident Fund tender source plug-in."""
import pytest


def test_raf_tenders_source_initialization():
    from tender_getter.sources.research_extra.raf_tenders import RafSource
    src = RafSource()
    assert src.source_id == "raf_tenders"
    assert src.live is True


def test_raf_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.raf_tenders import RafSource, MOCK_HTML
    src = RafSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_raf_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.raf_tenders import RafSource
    src = RafSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
