"""Tests for the Ditsong Museums of South Africa tender source plug-in."""
import pytest


def test_ditsong_source_initialization():
    from tender_getter.sources.research.ditsong import DitsongSource
    src = DitsongSource()
    assert src.source_id == "ditsong"
    assert isinstance(src.live, bool)


def test_ditsong_parse_mock_html():
    from tender_getter.sources.research.ditsong import DitsongSource, MOCK_HTML
    src = DitsongSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ditsong_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.ditsong import DitsongSource
    src = DitsongSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
