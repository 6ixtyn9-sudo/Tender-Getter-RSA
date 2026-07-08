"""Tests for the North West Health tender source plug-in."""
import pytest


def test_nw_health_tenders_source_initialization():
    from tender_getter.sources.research_extra.nw_health_tenders import NwHealthSource
    src = NwHealthSource()
    assert src.source_id == "nw_health_tenders"
    assert src.live is True


def test_nw_health_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.nw_health_tenders import NwHealthSource, MOCK_HTML
    src = NwHealthSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nw_health_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.nw_health_tenders import NwHealthSource
    src = NwHealthSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
