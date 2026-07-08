"""Tests for the Department of Transport tender source plug-in."""
import pytest


def test_dot_tenders_source_initialization():
    from tender_getter.sources.research_extra.dot_tenders import DotSource
    src = DotSource()
    assert src.source_id == "dot_tenders"
    assert src.live is True


def test_dot_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.dot_tenders import DotSource, MOCK_HTML
    src = DotSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dot_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.dot_tenders import DotSource
    src = DotSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
