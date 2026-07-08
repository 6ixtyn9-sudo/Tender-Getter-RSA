"""Tests for the Sarah Baartman District Municipality tender source plug-in."""
import pytest


def test_sarah_baartman_dm_source_initialization():
    from tender_getter.sources.districts.sarah_baartman_dm import SarahBaartmanDmSource
    src = SarahBaartmanDmSource()
    assert src.source_id == "sarah_baartman_dm"
    assert src.live is True


def test_sarah_baartman_dm_parse_mock_html():
    from tender_getter.sources.districts.sarah_baartman_dm import SarahBaartmanDmSource, MOCK_HTML
    src = SarahBaartmanDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sarah_baartman_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.sarah_baartman_dm import SarahBaartmanDmSource
    src = SarahBaartmanDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
