"""Tests for the Office of the Chief Justice (OCJ) tender source plug-in."""
import pytest


def test_ocj_source_initialization():
    from tender_getter.sources.schedule3a.ocj import OcjSource
    src = OcjSource()
    assert src.source_id == "ocj"
    assert isinstance(src.live, bool)


def test_ocj_parse_mock_html():
    from tender_getter.sources.schedule3a.ocj import OcjSource, MOCK_HTML
    src = OcjSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ocj_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.ocj import OcjSource
    src = OcjSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
