"""Tests for the Naturopathy Council tender source plug-in."""
import pytest


def test_naturopathy_council_source_initialization():
    from tender_getter.sources.research.naturopathy_council import NaturopathyCouncilSource
    src = NaturopathyCouncilSource()
    assert src.source_id == "naturopathy_council"
    assert isinstance(src.live, bool)


def test_naturopathy_council_parse_mock_html():
    from tender_getter.sources.research.naturopathy_council import NaturopathyCouncilSource, MOCK_HTML
    src = NaturopathyCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_naturopathy_council_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.naturopathy_council import NaturopathyCouncilSource
    src = NaturopathyCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
