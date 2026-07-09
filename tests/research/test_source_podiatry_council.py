"""Tests for the Podiatry Council tender source plug-in."""
import pytest


def test_podiatry_council_source_initialization():
    from tender_getter.sources.research.podiatry_council import PodiatryCouncilSource
    src = PodiatryCouncilSource()
    assert src.source_id == "podiatry_council"
    assert src.live is False


def test_podiatry_council_parse_mock_html():
    from tender_getter.sources.research.podiatry_council import PodiatryCouncilSource, MOCK_HTML
    src = PodiatryCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_podiatry_council_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.podiatry_council import PodiatryCouncilSource
    src = PodiatryCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
