"""Tests for the Pan South African Language Board (already in chapter9/) tender source plug-in."""
import pytest


def test_pan_sa_taal_source_initialization():
    from tender_getter.sources.research.pan_sa_taal import PanSaTaalSource
    src = PanSaTaalSource()
    assert src.source_id == "pan_sa_taal"
    assert isinstance(src.live, bool)


def test_pan_sa_taal_parse_mock_html():
    from tender_getter.sources.research.pan_sa_taal import PanSaTaalSource, MOCK_HTML
    src = PanSaTaalSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_pan_sa_taal_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.pan_sa_taal import PanSaTaalSource
    src = PanSaTaalSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
