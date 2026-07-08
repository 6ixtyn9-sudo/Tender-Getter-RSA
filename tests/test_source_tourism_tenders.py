"""Tests for the Department of Tourism tender source plug-in."""
import pytest


def test_tourism_tenders_source_initialization():
    from tender_getter.sources.research_extra.tourism_tenders import TourismSource
    src = TourismSource()
    assert src.source_id == "tourism_tenders"
    assert src.live is True


def test_tourism_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.tourism_tenders import TourismSource, MOCK_HTML
    src = TourismSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_tourism_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.tourism_tenders import TourismSource
    src = TourismSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
