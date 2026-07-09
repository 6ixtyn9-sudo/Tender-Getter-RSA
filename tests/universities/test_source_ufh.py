"""Tests for the University of Fort Hare tender source plug-in."""
import pytest


def test_ufh_source_initialization():
    from tender_getter.sources.universities.ufh import UfhSource
    src = UfhSource()
    assert src.source_id == "ufh"
    assert src.live is True


def test_ufh_parse_mock_html():
    from tender_getter.sources.universities.ufh import UfhSource, MOCK_HTML
    src = UfhSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ufh_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.ufh import UfhSource
    src = UfhSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
