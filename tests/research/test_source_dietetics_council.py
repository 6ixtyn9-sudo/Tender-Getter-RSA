"""Tests for the Dietetics Council tender source plug-in."""
import pytest


def test_dietetics_council_source_initialization():
    from tender_getter.sources.research.dietetics_council import DieteticsCouncilSource
    src = DieteticsCouncilSource()
    assert src.source_id == "dietetics_council"
    assert isinstance(src.live, bool)


def test_dietetics_council_parse_mock_html():
    from tender_getter.sources.research.dietetics_council import DieteticsCouncilSource, MOCK_HTML
    src = DieteticsCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dietetics_council_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.dietetics_council import DieteticsCouncilSource
    src = DieteticsCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
