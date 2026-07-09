"""Tests for the Eskom Rotek Industries tender source plug-in."""
import pytest


def test_eskom_rotek_source_initialization():
    from tender_getter.sources.soes.eskom_rotek import EskomRotekSource
    src = EskomRotekSource()
    assert src.source_id == "eskom_rotek"
    assert src.live is True


def test_eskom_rotek_parse_mock_html():
    from tender_getter.sources.soes.eskom_rotek import EskomRotekSource, MOCK_HTML
    src = EskomRotekSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_eskom_rotek_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.eskom_rotek import EskomRotekSource
    src = EskomRotekSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
