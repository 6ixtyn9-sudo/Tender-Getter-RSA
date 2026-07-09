"""Tests for the North West Development Corporation tender source plug-in."""
import pytest


def test_nw_dev_source_initialization():
    from tender_getter.sources.research.nw_dev import NwDevSource
    src = NwDevSource()
    assert src.source_id == "nw_dev"
    assert isinstance(src.live, bool)


def test_nw_dev_parse_mock_html():
    from tender_getter.sources.research.nw_dev import NwDevSource, MOCK_HTML
    src = NwDevSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nw_dev_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nw_dev import NwDevSource
    src = NwDevSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
