"""Tests for the Nasionale Pers tender source plug-in."""
import pytest


def test_nasionale_source_initialization():
    from tender_getter.sources.research.nasionale import NasionaleSource
    src = NasionaleSource()
    assert src.source_id == "nasionale"
    assert isinstance(src.live, bool)


def test_nasionale_parse_mock_html():
    from tender_getter.sources.research.nasionale import NasionaleSource, MOCK_HTML
    src = NasionaleSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nasionale_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nasionale import NasionaleSource
    src = NasionaleSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
