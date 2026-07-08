"""Tests for the West Coast District Municipality tender source plug-in."""
import pytest


def test_west_coast_dm_tenders_source_initialization():
    from tender_getter.sources.districts_full.west_coast_dm_tenders import WestCoastDmSource
    src = WestCoastDmSource()
    assert src.source_id == "west_coast_dm_tenders"
    assert src.live is True


def test_west_coast_dm_tenders_parse_mock_html():
    from tender_getter.sources.districts_full.west_coast_dm_tenders import WestCoastDmSource, MOCK_HTML
    src = WestCoastDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_west_coast_dm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts_full.west_coast_dm_tenders import WestCoastDmSource
    src = WestCoastDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
