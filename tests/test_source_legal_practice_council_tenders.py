"""Tests for the Legal Practice Council tender source plug-in."""
import pytest


def test_legal_practice_council_tenders_source_initialization():
    from tender_getter.sources.research_extra.legal_practice_council_tenders import LegalPracticeCouncilSource
    src = LegalPracticeCouncilSource()
    assert src.source_id == "legal_practice_council_tenders"
    assert src.live is True


def test_legal_practice_council_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.legal_practice_council_tenders import LegalPracticeCouncilSource, MOCK_HTML
    src = LegalPracticeCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_legal_practice_council_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.legal_practice_council_tenders import LegalPracticeCouncilSource
    src = LegalPracticeCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
