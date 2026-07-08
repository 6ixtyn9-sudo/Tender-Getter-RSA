"""Tests for the DFFE (alt) tender source plug-in."""
import pytest


def test_dffe_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.dffe_alt_tenders import DffeAltSource
    src = DffeAltSource()
    assert src.source_id == "dffe_alt_tenders"
    assert src.live is True


def test_dffe_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.dffe_alt_tenders import DffeAltSource, MOCK_HTML
    src = DffeAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dffe_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.dffe_alt_tenders import DffeAltSource
    src = DffeAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
