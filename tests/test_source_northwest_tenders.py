"""Tests for the North West Provincial Treasury tender source plug-in."""
import pytest


def test_northwest_tenders_source_initialization():
    from tender_getter.sources.research_extra.northwest_tenders import NorthwestSource
    src = NorthwestSource()
    assert src.source_id == "northwest_tenders"
    assert src.live is True


def test_northwest_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.northwest_tenders import NorthwestSource, MOCK_HTML
    src = NorthwestSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_northwest_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.northwest_tenders import NorthwestSource
    src = NorthwestSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
