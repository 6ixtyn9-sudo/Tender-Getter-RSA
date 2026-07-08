"""Tests for the Architectural Council tender source plug-in."""
import pytest


def test_architectural_council_tenders_source_initialization():
    from tender_getter.sources.research_extra.architectural_council_tenders import ArchitecturalCouncilSource
    src = ArchitecturalCouncilSource()
    assert src.source_id == "architectural_council_tenders"
    assert src.live is False


def test_architectural_council_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.architectural_council_tenders import ArchitecturalCouncilSource, MOCK_HTML
    src = ArchitecturalCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_architectural_council_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.architectural_council_tenders import ArchitecturalCouncilSource
    src = ArchitecturalCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
