"""Tests for the National Home Builders Registration Council (NHBRC) tender source plug-in."""
import pytest


def test_nhbrc_source_initialization():
    from tender_getter.sources.schedule3a.nhbrc import NhbrcSource
    src = NhbrcSource()
    assert src.source_id == "nhbrc"
    assert src.live is True


def test_nhbrc_parse_mock_html():
    from tender_getter.sources.schedule3a.nhbrc import NhbrcSource, MOCK_HTML
    src = NhbrcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nhbrc_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.nhbrc import NhbrcSource
    src = NhbrcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
