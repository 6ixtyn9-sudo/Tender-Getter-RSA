"""Tests for the Department of Women, Youth and Persons with Disabilities tender source plug-in."""
import pytest


def test_dwypd_tenders_source_initialization():
    from tender_getter.sources.schedule3a.dwypd_tenders import DwypdSource
    src = DwypdSource()
    assert src.source_id == "dwypd_tenders"
    assert src.live is True


def test_dwypd_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.dwypd_tenders import DwypdSource, MOCK_HTML
    src = DwypdSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dwypd_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.dwypd_tenders import DwypdSource
    src = DwypdSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
