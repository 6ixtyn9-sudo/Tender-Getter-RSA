"""Tests for the South African Police Service tender source plug-in."""
import pytest


def test_saps_tenders_source_initialization():
    from tender_getter.sources.research_extra.saps_tenders import SapsSource
    src = SapsSource()
    assert src.source_id == "saps_tenders"
    assert src.live is True


def test_saps_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.saps_tenders import SapsSource, MOCK_HTML
    src = SapsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_saps_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.saps_tenders import SapsSource
    src = SapsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
