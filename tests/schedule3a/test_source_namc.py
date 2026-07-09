"""Tests for the National Agricultural Marketing Council (NAMC) tender source plug-in."""
import pytest


def test_namc_source_initialization():
    from tender_getter.sources.schedule3a.namc import NamcSource
    src = NamcSource()
    assert src.source_id == "namc"
    assert isinstance(src.live, bool)


def test_namc_parse_mock_html():
    from tender_getter.sources.schedule3a.namc import NamcSource, MOCK_HTML
    src = NamcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_namc_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.namc import NamcSource
    src = NamcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
