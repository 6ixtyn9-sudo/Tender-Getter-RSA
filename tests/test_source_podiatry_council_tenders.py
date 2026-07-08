"""Tests for the Podiatry Council tender source plug-in."""
import pytest


def test_podiatry_council_tenders_source_initialization():
    from tender_getter.sources.research_extra.podiatry_council_tenders import PodiatryCouncilSource
    src = PodiatryCouncilSource()
    assert src.source_id == "podiatry_council_tenders"
    assert src.live is False


def test_podiatry_council_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.podiatry_council_tenders import PodiatryCouncilSource, MOCK_HTML
    src = PodiatryCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_podiatry_council_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.podiatry_council_tenders import PodiatryCouncilSource
    src = PodiatryCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
