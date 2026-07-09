"""Tests for the CGSI tender source plug-in."""
import pytest


def test_cgsi_source_initialization():
    from tender_getter.sources.research.cgsi import CgsiSource
    src = CgsiSource()
    assert src.source_id == "cgsi"
    assert isinstance(src.live, bool)


def test_cgsi_parse_mock_html():
    from tender_getter.sources.research.cgsi import CgsiSource, MOCK_HTML
    src = CgsiSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_cgsi_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.cgsi import CgsiSource
    src = CgsiSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
