"""Tests for the OT Council tender source plug-in."""
import pytest


def test_occupational_therapy_council_tenders_source_initialization():
    from tender_getter.sources.research_extra.occupational_therapy_council_tenders import OccupationalTherapyCouncilSource
    src = OccupationalTherapyCouncilSource()
    assert src.source_id == "occupational_therapy_council_tenders"
    assert src.live is False


def test_occupational_therapy_council_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.occupational_therapy_council_tenders import OccupationalTherapyCouncilSource, MOCK_HTML
    src = OccupationalTherapyCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_occupational_therapy_council_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.occupational_therapy_council_tenders import OccupationalTherapyCouncilSource
    src = OccupationalTherapyCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
