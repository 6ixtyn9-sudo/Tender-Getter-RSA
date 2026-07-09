"""Tests for the University of Limpopo tender source plug-in."""
import pytest


def test_ul_source_initialization():
    from tender_getter.sources.universities.ul import UlSource
    src = UlSource()
    assert src.source_id == "ul"
    assert isinstance(src.live, bool)


def test_ul_parse_mock_html():
    from tender_getter.sources.universities.ul import UlSource, MOCK_HTML
    src = UlSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ul_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.ul import UlSource
    src = UlSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
