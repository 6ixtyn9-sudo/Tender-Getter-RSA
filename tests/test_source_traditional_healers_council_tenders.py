"""Tests for the Traditional Healers Council tender source plug-in."""
import pytest


def test_traditional_healers_council_tenders_source_initialization():
    from tender_getter.sources.research_extra.traditional_healers_council_tenders import TraditionalHealersCouncilSource
    src = TraditionalHealersCouncilSource()
    assert src.source_id == "traditional_healers_council_tenders"
    assert src.live is False


def test_traditional_healers_council_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.traditional_healers_council_tenders import TraditionalHealersCouncilSource, MOCK_HTML
    src = TraditionalHealersCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_traditional_healers_council_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.traditional_healers_council_tenders import TraditionalHealersCouncilSource
    src = TraditionalHealersCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
