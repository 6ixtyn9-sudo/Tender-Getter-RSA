"""Tests for the Pitso ya Marena tender source plug-in."""
import pytest


def test_pitso_source_initialization():
    from tender_getter.sources.research.pitso import PitsoSource
    src = PitsoSource()
    assert src.source_id == "pitso"
    assert isinstance(src.live, bool)


def test_pitso_parse_mock_html():
    from tender_getter.sources.research.pitso import PitsoSource, MOCK_HTML
    src = PitsoSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_pitso_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.pitso import PitsoSource
    src = PitsoSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
