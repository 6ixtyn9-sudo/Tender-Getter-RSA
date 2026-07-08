"""Tests for the South African National Energy Development Institute (SANEDI) tender source plug-in."""
import pytest


def test_sanedi_tenders_source_initialization():
    from tender_getter.sources.schedule3a.sanedi_tenders import SanediSource
    src = SanediSource()
    assert src.source_id == "sanedi_tenders"
    assert src.live is True


def test_sanedi_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.sanedi_tenders import SanediSource, MOCK_HTML
    src = SanediSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sanedi_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.sanedi_tenders import SanediSource
    src = SanediSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
