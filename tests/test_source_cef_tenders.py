"""Tests for the Central Energy Fund (CEF) SOC Ltd tender source plug-in."""
import pytest


def test_cef_tenders_source_initialization():
    from tender_getter.sources.soes_extra.cef_tenders import CefSource
    src = CefSource()
    assert src.source_id == "cef_tenders"
    assert src.live is True


def test_cef_tenders_parse_mock_html():
    from tender_getter.sources.soes_extra.cef_tenders import CefSource, MOCK_HTML
    src = CefSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_cef_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes_extra.cef_tenders import CefSource
    src = CefSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
