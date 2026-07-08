"""Tests for the Walter Sisulu University tender source plug-in."""
import pytest


def test_wsu_source_initialization():
    from tender_getter.sources.universities.wsu import WsuSource
    src = WsuSource()
    assert src.source_id == "wsu"
    assert src.live is True


def test_wsu_parse_mock_html():
    from tender_getter.sources.universities.wsu import WsuSource, MOCK_HTML
    src = WsuSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wsu_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.wsu import WsuSource
    src = WsuSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
