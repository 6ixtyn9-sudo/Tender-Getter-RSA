"""Tests for the ECSA (alt) tender source plug-in."""
import pytest


def test_engineering_council_tenders_source_initialization():
    from tender_getter.sources.research_extra.engineering_council_tenders import EngineeringCouncilSource
    src = EngineeringCouncilSource()
    assert src.source_id == "engineering_council_tenders"
    assert src.live is True


def test_engineering_council_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.engineering_council_tenders import EngineeringCouncilSource, MOCK_HTML
    src = EngineeringCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_engineering_council_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.engineering_council_tenders import EngineeringCouncilSource
    src = EngineeringCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
