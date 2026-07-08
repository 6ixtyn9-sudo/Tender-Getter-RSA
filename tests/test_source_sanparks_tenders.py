"""Tests for the South African National Parks tender source plug-in."""
import pytest


def test_sanparks_tenders_source_initialization():
    from tender_getter.sources.research_extra.sanparks_tenders import SanparksSource
    src = SanparksSource()
    assert src.source_id == "sanparks_tenders"
    assert src.live is True


def test_sanparks_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.sanparks_tenders import SanparksSource, MOCK_HTML
    src = SanparksSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sanparks_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.sanparks_tenders import SanparksSource
    src = SanparksSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
