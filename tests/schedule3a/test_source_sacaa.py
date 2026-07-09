"""Tests for the South African Civil Aviation Authority (SACAA) tender source plug-in."""
import pytest


def test_sacaa_source_initialization():
    from tender_getter.sources.schedule3a.sacaa import SacaaSource
    src = SacaaSource()
    assert src.source_id == "sacaa"
    assert isinstance(src.live, bool)


def test_sacaa_parse_mock_html():
    from tender_getter.sources.schedule3a.sacaa import SacaaSource, MOCK_HTML
    src = SacaaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sacaa_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.sacaa import SacaaSource
    src = SacaaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
