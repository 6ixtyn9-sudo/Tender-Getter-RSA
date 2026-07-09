"""Tests for the iThemba Laboratory for Accelerator Based Sciences tender source plug-in."""
import pytest


def test_ithemba_source_initialization():
    from tender_getter.sources.research.ithemba import IthembaSource
    src = IthembaSource()
    assert src.source_id == "ithemba"
    assert isinstance(src.live, bool)


def test_ithemba_parse_mock_html():
    from tender_getter.sources.research.ithemba import IthembaSource, MOCK_HTML
    src = IthembaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ithemba_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.ithemba import IthembaSource
    src = IthembaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
