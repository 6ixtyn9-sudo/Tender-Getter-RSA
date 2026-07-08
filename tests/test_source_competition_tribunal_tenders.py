"""Tests for the Competition Tribunal tender source plug-in."""
import pytest


def test_competition_tribunal_tenders_source_initialization():
    from tender_getter.sources.research_extra.competition_tribunal_tenders import CompetitionTribunalSource
    src = CompetitionTribunalSource()
    assert src.source_id == "competition_tribunal_tenders"
    assert src.live is False


def test_competition_tribunal_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.competition_tribunal_tenders import CompetitionTribunalSource, MOCK_HTML
    src = CompetitionTribunalSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_competition_tribunal_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.competition_tribunal_tenders import CompetitionTribunalSource
    src = CompetitionTribunalSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
