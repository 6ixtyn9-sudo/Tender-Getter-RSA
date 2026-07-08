"""Tests for the West Rand District Municipality tender source plug-in."""
import pytest


def test_west_rand_tenders_source_initialization():
    from tender_getter.sources.research_extra.west_rand_tenders import WestRandSource
    src = WestRandSource()
    assert src.source_id == "west_rand_tenders"
    assert src.live is True


def test_west_rand_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.west_rand_tenders import WestRandSource, MOCK_HTML
    src = WestRandSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_west_rand_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.west_rand_tenders import WestRandSource
    src = WestRandSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
