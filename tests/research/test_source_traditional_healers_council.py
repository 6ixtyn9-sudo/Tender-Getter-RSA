"""Tests for the Traditional Healers Council tender source plug-in."""
import pytest


def test_traditional_healers_council_source_initialization():
    from tender_getter.sources.research.traditional_healers_council import TraditionalHealersCouncilSource
    src = TraditionalHealersCouncilSource()
    assert src.source_id == "traditional_healers_council"
    assert isinstance(src.live, bool)


def test_traditional_healers_council_parse_mock_html():
    from tender_getter.sources.research.traditional_healers_council import TraditionalHealersCouncilSource, MOCK_HTML
    src = TraditionalHealersCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_traditional_healers_council_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.traditional_healers_council import TraditionalHealersCouncilSource
    src = TraditionalHealersCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
