"""Tests for the National Research Foundation (NRF) tender source plug-in."""
import pytest


def test_nrf_source_initialization():
    from tender_getter.sources.research.nrf import NrfSource
    src = NrfSource()
    assert src.source_id == "nrf"
    assert isinstance(src.live, bool)


def test_nrf_parse_mock_html():
    from tender_getter.sources.research.nrf import NrfSource, MOCK_HTML
    src = NrfSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nrf_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.nrf import NrfSource
    src = NrfSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
