"""Tests for the Department of Employment and Labour tender source plug-in."""
import pytest


def test_doel_tenders_source_initialization():
    from tender_getter.sources.research_extra.doel_tenders import DoelSource
    src = DoelSource()
    assert src.source_id == "doel_tenders"
    assert src.live is True


def test_doel_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.doel_tenders import DoelSource, MOCK_HTML
    src = DoelSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_doel_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.doel_tenders import DoelSource
    src = DoelSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
