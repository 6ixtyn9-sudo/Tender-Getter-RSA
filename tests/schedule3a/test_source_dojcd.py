"""Tests for the Department of Justice and Constitutional Development tender source plug-in."""
import pytest


def test_dojcd_source_initialization():
    from tender_getter.sources.schedule3a.dojcd import DojcdSource
    src = DojcdSource()
    assert src.source_id == "dojcd"
    assert src.live is True


def test_dojcd_parse_mock_html():
    from tender_getter.sources.schedule3a.dojcd import DojcdSource, MOCK_HTML
    src = DojcdSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dojcd_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.dojcd import DojcdSource
    src = DojcdSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
