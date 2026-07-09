"""Tests for the Coega Development Corporation (CDC) tender source plug-in."""
import pytest


def test_coega_source_initialization():
    from tender_getter.sources.soes.coega import CoegaSource
    src = CoegaSource()
    assert src.source_id == "coega"
    assert src.live is True


def test_coega_parse_mock_html():
    from tender_getter.sources.soes.coega import CoegaSource, MOCK_HTML
    src = CoegaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_coega_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.coega import CoegaSource
    src = CoegaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
