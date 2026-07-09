"""Tests for the Transnet National Ports Authority (TNPA) tender source plug-in."""
import pytest


def test_tnpa_source_initialization():
    from tender_getter.sources.soes.tnpa import TnpaSource
    src = TnpaSource()
    assert src.source_id == "tnpa"
    assert src.live is True


def test_tnpa_parse_mock_html():
    from tender_getter.sources.soes.tnpa import TnpaSource, MOCK_HTML
    src = TnpaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_tnpa_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.tnpa import TnpaSource
    src = TnpaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
