"""Tests for the Joe Gqabi District Municipality tender source plug-in."""
import pytest


def test_joe_gqabi_dm_source_initialization():
    from tender_getter.sources.districts.joe_gqabi_dm import JoeGqabiDmSource
    src = JoeGqabiDmSource()
    assert src.source_id == "joe_gqabi_dm"
    assert src.live is True


def test_joe_gqabi_dm_parse_mock_html():
    from tender_getter.sources.districts.joe_gqabi_dm import JoeGqabiDmSource, MOCK_HTML
    src = JoeGqabiDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_joe_gqabi_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.joe_gqabi_dm import JoeGqabiDmSource
    src = JoeGqabiDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
