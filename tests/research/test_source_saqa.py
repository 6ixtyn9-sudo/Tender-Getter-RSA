"""Tests for the SAQA tender source plug-in."""
import pytest


def test_saqa_source_initialization():
    from tender_getter.sources.research.saqa import SaqaSource
    src = SaqaSource()
    assert src.source_id == "saqa"
    assert isinstance(src.live, bool)


def test_saqa_parse_mock_html():
    from tender_getter.sources.research.saqa import SaqaSource, MOCK_HTML
    src = SaqaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_saqa_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.saqa import SaqaSource
    src = SaqaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
