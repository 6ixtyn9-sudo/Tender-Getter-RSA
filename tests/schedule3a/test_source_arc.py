"""Tests for the Agricultural Research Council (ARC) tender source plug-in."""
import pytest


def test_arc_source_initialization():
    from tender_getter.sources.schedule3a.arc import ArcSource
    src = ArcSource()
    assert src.source_id == "arc"
    assert isinstance(src.live, bool)


def test_arc_parse_mock_html():
    from tender_getter.sources.schedule3a.arc import ArcSource, MOCK_HTML
    src = ArcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_arc_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.arc import ArcSource
    src = ArcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
