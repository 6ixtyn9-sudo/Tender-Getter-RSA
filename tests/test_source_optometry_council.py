"""Tests for the Optometry Council tender source plug-in."""
import pytest


def test_optometry_council_source_initialization():
    from tender_getter.sources.research.optometry_council import OptometryCouncilSource
    src = OptometryCouncilSource()
    assert src.source_id == "optometry_council"
    assert src.live is False


def test_optometry_council_parse_mock_html():
    from tender_getter.sources.research.optometry_council import OptometryCouncilSource, MOCK_HTML
    src = OptometryCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_optometry_council_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.optometry_council import OptometryCouncilSource
    src = OptometryCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
