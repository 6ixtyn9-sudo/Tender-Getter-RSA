"""Tests for the Ditsong Museums of South Africa tender source plug-in."""
import pytest


def test_ditsong_tenders_source_initialization():
    from tender_getter.sources.research_extra.ditsong_tenders import DitsongSource
    src = DitsongSource()
    assert src.source_id == "ditsong_tenders"
    assert src.live is True


def test_ditsong_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.ditsong_tenders import DitsongSource, MOCK_HTML
    src = DitsongSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ditsong_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.ditsong_tenders import DitsongSource
    src = DitsongSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
