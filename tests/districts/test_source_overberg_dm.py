"""Tests for the Overberg District Municipality tender source plug-in."""
import pytest


def test_overberg_dm_source_initialization():
    from tender_getter.sources.districts.overberg_dm import OverbergDmSource
    src = OverbergDmSource()
    assert src.source_id == "overberg_dm"
    assert isinstance(src.live, bool)


def test_overberg_dm_parse_mock_html():
    from tender_getter.sources.districts.overberg_dm import OverbergDmSource, MOCK_HTML
    src = OverbergDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_overberg_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.overberg_dm import OverbergDmSource
    src = OverbergDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
