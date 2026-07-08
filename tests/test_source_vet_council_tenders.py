"""Tests for the Vet Council tender source plug-in."""
import pytest


def test_vet_council_tenders_source_initialization():
    from tender_getter.sources.research_extra.vet_council_tenders import VetCouncilSource
    src = VetCouncilSource()
    assert src.source_id == "vet_council_tenders"
    assert src.live is False


def test_vet_council_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.vet_council_tenders import VetCouncilSource, MOCK_HTML
    src = VetCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_vet_council_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.vet_council_tenders import VetCouncilSource
    src = VetCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
