"""Tests for the Agricultural Research Council (ARC) tender source plug-in."""
import pytest


def test_arc_tenders_source_initialization():
    from tender_getter.sources.schedule3a.arc_tenders import ArcSource
    src = ArcSource()
    assert src.source_id == "arc_tenders"
    assert src.live is True


def test_arc_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.arc_tenders import ArcSource, MOCK_HTML
    src = ArcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_arc_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.arc_tenders import ArcSource
    src = ArcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
