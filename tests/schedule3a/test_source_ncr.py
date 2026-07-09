"""Tests for the National Credit Regulator (NCR) tender source plug-in."""
import pytest


def test_ncr_source_initialization():
    from tender_getter.sources.schedule3a.ncr import NcrSource
    src = NcrSource()
    assert src.source_id == "ncr"
    assert isinstance(src.live, bool)


def test_ncr_parse_mock_html():
    from tender_getter.sources.schedule3a.ncr import NcrSource, MOCK_HTML
    src = NcrSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ncr_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.ncr import NcrSource
    src = NcrSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
