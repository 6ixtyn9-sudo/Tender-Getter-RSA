"""Tests for the Financial Sector Conduct Authority (FSCA) tender source plug-in."""
import pytest


def test_fsc_source_initialization():
    from tender_getter.sources.schedule3a.fsc import FscSource
    src = FscSource()
    assert src.source_id == "fsc"
    assert isinstance(src.live, bool)


def test_fsc_parse_mock_html():
    from tender_getter.sources.schedule3a.fsc import FscSource, MOCK_HTML
    src = FscSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fsc_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.fsc import FscSource
    src = FscSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
