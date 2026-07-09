"""Tests for the South African National Energy Development Institute (SANEDI) tender source plug-in."""
import pytest


def test_sanedi_source_initialization():
    from tender_getter.sources.schedule3a.sanedi import SanediSource
    src = SanediSource()
    assert src.source_id == "sanedi"
    assert isinstance(src.live, bool)


def test_sanedi_parse_mock_html():
    from tender_getter.sources.schedule3a.sanedi import SanediSource, MOCK_HTML
    src = SanediSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sanedi_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.sanedi import SanediSource
    src = SanediSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
