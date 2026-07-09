"""Tests for the Department of Social Development tender source plug-in."""
import pytest


def test_dsd_source_initialization():
    from tender_getter.sources.schedule3a.dsd import DsdSource
    src = DsdSource()
    assert src.source_id == "dsd"
    assert isinstance(src.live, bool)


def test_dsd_parse_mock_html():
    from tender_getter.sources.schedule3a.dsd import DsdSource, MOCK_HTML
    src = DsdSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dsd_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.dsd import DsdSource
    src = DsdSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
