"""Tests for the National Prosecuting Authority (NPA) tender source plug-in."""
import pytest


def test_npa_source_initialization():
    from tender_getter.sources.soes.npa import NpaSource
    src = NpaSource()
    assert src.source_id == "npa"
    assert src.live is True


def test_npa_parse_mock_html():
    from tender_getter.sources.soes.npa import NpaSource, MOCK_HTML
    src = NpaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_npa_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.npa import NpaSource
    src = NpaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
