"""Tests for the Pharma Council tender source plug-in."""
import pytest


def test_pharma_council_source_initialization():
    from tender_getter.sources.research.pharma_council import PharmaCouncilSource
    src = PharmaCouncilSource()
    assert src.source_id == "pharma_council"
    assert src.live is True


def test_pharma_council_parse_mock_html():
    from tender_getter.sources.research.pharma_council import PharmaCouncilSource, MOCK_HTML
    src = PharmaCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_pharma_council_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.pharma_council import PharmaCouncilSource
    src = PharmaCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
