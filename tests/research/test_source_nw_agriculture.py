"""Tests for the North West Agriculture tender source plug-in."""
import pytest


def test_nw_agriculture_source_initialization():
    from tender_getter.sources.research.nw_agriculture import NwAgricultureSource
    src = NwAgricultureSource()
    assert src.source_id == "nw_agriculture"
    assert isinstance(src.live, bool)


def test_nw_agriculture_parse_mock_html():
    from tender_getter.sources.research.nw_agriculture import NwAgricultureSource, MOCK_HTML
    src = NwAgricultureSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nw_agriculture_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nw_agriculture import NwAgricultureSource
    src = NwAgricultureSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
