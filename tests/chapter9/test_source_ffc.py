"""Tests for the Financial and Fiscal Commission (FFC) tender source plug-in."""
import pytest


def test_ffc_source_initialization():
    from tender_getter.sources.chapter9.ffc import FfcSource
    src = FfcSource()
    assert src.source_id == "ffc"
    assert isinstance(src.live, bool)


def test_ffc_parse_mock_html():
    from tender_getter.sources.chapter9.ffc import FfcSource, MOCK_HTML
    src = FfcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ffc_fetch_uses_fallback_on_empty():
    from tender_getter.sources.chapter9.ffc import FfcSource
    src = FfcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
