"""Tests for the Denel Maritime tender source plug-in."""
import pytest


def test_denel_maritime_source_initialization():
    from tender_getter.sources.soes.denel_maritime import DenelMaritimeSource
    src = DenelMaritimeSource()
    assert src.source_id == "denel_maritime"
    assert isinstance(src.live, bool)


def test_denel_maritime_parse_mock_html():
    from tender_getter.sources.soes.denel_maritime import DenelMaritimeSource, MOCK_HTML
    src = DenelMaritimeSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_denel_maritime_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.denel_maritime import DenelMaritimeSource
    src = DenelMaritimeSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
