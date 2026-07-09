"""Tests for the Iziko Museums of South Africa tender source plug-in."""
import pytest


def test_iziko_source_initialization():
    from tender_getter.sources.research.iziko import IzikoSource
    src = IzikoSource()
    assert src.source_id == "iziko"
    assert src.live is True


def test_iziko_parse_mock_html():
    from tender_getter.sources.research.iziko import IzikoSource, MOCK_HTML
    src = IzikoSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_iziko_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.iziko import IzikoSource
    src = IzikoSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
