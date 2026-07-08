"""Tests for the Radiography Council tender source plug-in."""
import pytest


def test_radiography_council_source_initialization():
    from tender_getter.sources.research.radiography_council import RadiographyCouncilSource
    src = RadiographyCouncilSource()
    assert src.source_id == "radiography_council"
    assert src.live is False


def test_radiography_council_parse_mock_html():
    from tender_getter.sources.research.radiography_council import RadiographyCouncilSource, MOCK_HTML
    src = RadiographyCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_radiography_council_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.radiography_council import RadiographyCouncilSource
    src = RadiographyCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
