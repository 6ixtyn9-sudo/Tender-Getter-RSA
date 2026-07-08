"""Tests for the Chris Hani District Municipality tender source plug-in."""
import pytest


def test_chris_hani_dm_tenders_source_initialization():
    from tender_getter.sources.districts_full.chris_hani_dm_tenders import ChrisHaniDmSource
    src = ChrisHaniDmSource()
    assert src.source_id == "chris_hani_dm_tenders"
    assert src.live is True


def test_chris_hani_dm_tenders_parse_mock_html():
    from tender_getter.sources.districts_full.chris_hani_dm_tenders import ChrisHaniDmSource, MOCK_HTML
    src = ChrisHaniDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_chris_hani_dm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts_full.chris_hani_dm_tenders import ChrisHaniDmSource
    src = ChrisHaniDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
