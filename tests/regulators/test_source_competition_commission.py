"""Tests for the Competition Commission tender source plug-in."""
import pytest


def test_competition_commission_source_initialization():
    from tender_getter.sources.regulators.competition_commission import CompetitionCommissionSource
    src = CompetitionCommissionSource()
    assert src.source_id == "competition_commission"
    assert isinstance(src.live, bool)


def test_competition_commission_parse_mock_html():
    from tender_getter.sources.regulators.competition_commission import CompetitionCommissionSource, MOCK_HTML
    src = CompetitionCommissionSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_competition_commission_fetch_uses_fallback_on_empty():
    from tender_getter.sources.regulators.competition_commission import CompetitionCommissionSource
    src = CompetitionCommissionSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
