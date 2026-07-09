"""Tests for the Biokinetics Council tender source plug-in."""
import pytest


def test_biokinetics_council_source_initialization():
    from tender_getter.sources.research.biokinetics_council import BiokineticsCouncilSource
    src = BiokineticsCouncilSource()
    assert src.source_id == "biokinetics_council"
    assert src.live is False


def test_biokinetics_council_parse_mock_html():
    from tender_getter.sources.research.biokinetics_council import BiokineticsCouncilSource, MOCK_HTML
    src = BiokineticsCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_biokinetics_council_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.biokinetics_council import BiokineticsCouncilSource
    src = BiokineticsCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
