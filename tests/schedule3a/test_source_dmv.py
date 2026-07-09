"""Tests for the Department of Military Veterans tender source plug-in."""
import pytest


def test_dmv_source_initialization():
    from tender_getter.sources.schedule3a.dmv import DmvSource
    src = DmvSource()
    assert src.source_id == "dmv"
    assert isinstance(src.live, bool)


def test_dmv_parse_mock_html():
    from tender_getter.sources.schedule3a.dmv import DmvSource, MOCK_HTML
    src = DmvSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dmv_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.dmv import DmvSource
    src = DmvSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
