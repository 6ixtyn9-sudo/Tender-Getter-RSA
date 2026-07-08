"""Tests for the Nursing Council (alt) tender source plug-in."""
import pytest


def test_nursing_council_tenders_source_initialization():
    from tender_getter.sources.research_extra.nursing_council_tenders import NursingCouncilSource
    src = NursingCouncilSource()
    assert src.source_id == "nursing_council_tenders"
    assert src.live is True


def test_nursing_council_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.nursing_council_tenders import NursingCouncilSource, MOCK_HTML
    src = NursingCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nursing_council_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.nursing_council_tenders import NursingCouncilSource
    src = NursingCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
