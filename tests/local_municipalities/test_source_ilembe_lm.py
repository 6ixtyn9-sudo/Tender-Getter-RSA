"""Tests for the iLembe District Municipality (LM form) tender source plug-in."""
import pytest


def test_ilembe_lm_source_initialization():
    from tender_getter.sources.local_municipalities.ilembe_lm import IlembeLmSource
    src = IlembeLmSource()
    assert src.source_id == "ilembe_lm"
    assert isinstance(src.live, bool)


def test_ilembe_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.ilembe_lm import IlembeLmSource, MOCK_HTML
    src = IlembeLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ilembe_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ilembe_lm import IlembeLmSource
    src = IlembeLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
