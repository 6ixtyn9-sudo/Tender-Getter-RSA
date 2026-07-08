"""Tests for the Ayurveda Council tender source plug-in."""
import pytest


def test_ayurveda_council_tenders_source_initialization():
    from tender_getter.sources.research_extra.ayurveda_council_tenders import AyurvedaCouncilSource
    src = AyurvedaCouncilSource()
    assert src.source_id == "ayurveda_council_tenders"
    assert src.live is False


def test_ayurveda_council_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.ayurveda_council_tenders import AyurvedaCouncilSource, MOCK_HTML
    src = AyurvedaCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ayurveda_council_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.ayurveda_council_tenders import AyurvedaCouncilSource
    src = AyurvedaCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
