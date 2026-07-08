"""Tests for the North West Tourism Board tender source plug-in."""
import pytest


def test_nw_tourism_tenders_source_initialization():
    from tender_getter.sources.research_extra.nw_tourism_tenders import NwTourismSource
    src = NwTourismSource()
    assert src.source_id == "nw_tourism_tenders"
    assert src.live is False


def test_nw_tourism_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.nw_tourism_tenders import NwTourismSource, MOCK_HTML
    src = NwTourismSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nw_tourism_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.nw_tourism_tenders import NwTourismSource
    src = NwTourismSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
