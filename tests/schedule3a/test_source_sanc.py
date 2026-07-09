"""Tests for the South African Nursing Council (SANC) tender source plug-in."""
import pytest


def test_sanc_source_initialization():
    from tender_getter.sources.schedule3a.sanc import SancSource
    src = SancSource()
    assert src.source_id == "sanc"
    assert isinstance(src.live, bool)


def test_sanc_parse_mock_html():
    from tender_getter.sources.schedule3a.sanc import SancSource, MOCK_HTML
    src = SancSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sanc_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.sanc import SancSource
    src = SancSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
