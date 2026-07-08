"""Tests for the Osteopathy Council tender source plug-in."""
import pytest


def test_osteopathy_council_tenders_source_initialization():
    from tender_getter.sources.research_extra.osteopathy_council_tenders import OsteopathyCouncilSource
    src = OsteopathyCouncilSource()
    assert src.source_id == "osteopathy_council_tenders"
    assert src.live is False


def test_osteopathy_council_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.osteopathy_council_tenders import OsteopathyCouncilSource, MOCK_HTML
    src = OsteopathyCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_osteopathy_council_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.osteopathy_council_tenders import OsteopathyCouncilSource
    src = OsteopathyCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
