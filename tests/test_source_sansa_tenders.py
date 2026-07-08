"""Tests for the South African National Space Agency tender source plug-in."""
import pytest


def test_sansa_tenders_source_initialization():
    from tender_getter.sources.research_extra.sansa_tenders import SansaSource
    src = SansaSource()
    assert src.source_id == "sansa_tenders"
    assert src.live is True


def test_sansa_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.sansa_tenders import SansaSource, MOCK_HTML
    src = SansaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sansa_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.sansa_tenders import SansaSource
    src = SansaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
