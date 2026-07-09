"""Tests for the ICA (SA) tender source plug-in."""
import pytest


def test_ica_source_initialization():
    from tender_getter.sources.research.ica import IcaSource
    src = IcaSource()
    assert src.source_id == "ica"
    assert src.live is False


def test_ica_parse_mock_html():
    from tender_getter.sources.research.ica import IcaSource, MOCK_HTML
    src = IcaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ica_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.ica import IcaSource
    src = IcaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
