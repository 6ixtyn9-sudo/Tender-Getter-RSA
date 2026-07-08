"""Tests for the NEHAWU tender source plug-in."""
import pytest


def test_nehawu_source_initialization():
    from tender_getter.sources.research.nehawu import NehawuSource
    src = NehawuSource()
    assert src.source_id == "nehawu"
    assert src.live is False


def test_nehawu_parse_mock_html():
    from tender_getter.sources.research.nehawu import NehawuSource, MOCK_HTML
    src = NehawuSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nehawu_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nehawu import NehawuSource
    src = NehawuSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
