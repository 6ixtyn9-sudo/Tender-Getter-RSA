"""Tests for the Department of Women, Youth and Persons with Disabilities tender source plug-in."""
import pytest


def test_dwypd_source_initialization():
    from tender_getter.sources.schedule3a.dwypd import DwypdSource
    src = DwypdSource()
    assert src.source_id == "dwypd"
    assert isinstance(src.live, bool)


def test_dwypd_parse_mock_html():
    from tender_getter.sources.schedule3a.dwypd import DwypdSource, MOCK_HTML
    src = DwypdSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dwypd_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.dwypd import DwypdSource
    src = DwypdSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
