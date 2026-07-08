"""Tests for the Homeopathy Council tender source plug-in."""
import pytest


def test_homeopathy_council_source_initialization():
    from tender_getter.sources.research.homeopathy_council import HomeopathyCouncilSource
    src = HomeopathyCouncilSource()
    assert src.source_id == "homeopathy_council"
    assert src.live is False


def test_homeopathy_council_parse_mock_html():
    from tender_getter.sources.research.homeopathy_council import HomeopathyCouncilSource, MOCK_HTML
    src = HomeopathyCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_homeopathy_council_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.homeopathy_council import HomeopathyCouncilSource
    src = HomeopathyCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
