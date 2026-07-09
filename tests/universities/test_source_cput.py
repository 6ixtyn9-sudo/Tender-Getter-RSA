"""Tests for the Cape Peninsula University of Technology tender source plug-in."""
import pytest


def test_cput_source_initialization():
    from tender_getter.sources.universities.cput import CputSource
    src = CputSource()
    assert src.source_id == "cput"
    assert isinstance(src.live, bool)


def test_cput_parse_mock_html():
    from tender_getter.sources.universities.cput import CputSource, MOCK_HTML
    src = CputSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_cput_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.cput import CputSource
    src = CputSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
