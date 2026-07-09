"""Tests for the SA Federation of Oil Trading Companies tender source plug-in."""
import pytest


def test_safo_source_initialization():
    from tender_getter.sources.research.safo import SafoSource
    src = SafoSource()
    assert src.source_id == "safo"
    assert isinstance(src.live, bool)


def test_safo_parse_mock_html():
    from tender_getter.sources.research.safo import SafoSource, MOCK_HTML
    src = SafoSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_safo_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.safo import SafoSource
    src = SafoSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
