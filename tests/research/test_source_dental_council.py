"""Tests for the Dental Council tender source plug-in."""
import pytest


def test_dental_council_source_initialization():
    from tender_getter.sources.research.dental_council import DentalCouncilSource
    src = DentalCouncilSource()
    assert src.source_id == "dental_council"
    assert isinstance(src.live, bool)


def test_dental_council_parse_mock_html():
    from tender_getter.sources.research.dental_council import DentalCouncilSource, MOCK_HTML
    src = DentalCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dental_council_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.dental_council import DentalCouncilSource
    src = DentalCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
