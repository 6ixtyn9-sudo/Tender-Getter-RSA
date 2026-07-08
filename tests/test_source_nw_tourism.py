"""Tests for the North West Tourism Board tender source plug-in."""
import pytest


def test_nw_tourism_source_initialization():
    from tender_getter.sources.research.nw_tourism import NwTourismSource
    src = NwTourismSource()
    assert src.source_id == "nw_tourism"
    assert src.live is False


def test_nw_tourism_parse_mock_html():
    from tender_getter.sources.research.nw_tourism import NwTourismSource, MOCK_HTML
    src = NwTourismSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nw_tourism_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nw_tourism import NwTourismSource
    src = NwTourismSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
