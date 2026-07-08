"""Tests for the Council for Geoscience tender source plug-in."""
import pytest


def test_geoscience_tenders_source_initialization():
    from tender_getter.sources.research_extra.geoscience_tenders import GeoscienceSource
    src = GeoscienceSource()
    assert src.source_id == "geoscience_tenders"
    assert src.live is True


def test_geoscience_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.geoscience_tenders import GeoscienceSource, MOCK_HTML
    src = GeoscienceSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_geoscience_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.geoscience_tenders import GeoscienceSource
    src = GeoscienceSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
