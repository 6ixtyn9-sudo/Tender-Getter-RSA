"""Tests for the Allied Health Council tender source plug-in."""
import pytest


def test_allied_health_council_source_initialization():
    from tender_getter.sources.research.allied_health_council import AlliedHealthCouncilSource
    src = AlliedHealthCouncilSource()
    assert src.source_id == "allied_health_council"
    assert src.live is False


def test_allied_health_council_parse_mock_html():
    from tender_getter.sources.research.allied_health_council import AlliedHealthCouncilSource, MOCK_HTML
    src = AlliedHealthCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_allied_health_council_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.allied_health_council import AlliedHealthCouncilSource
    src = AlliedHealthCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
