"""Tests for the Mossel Bay (alt) tender source plug-in."""
import pytest


def test_mossel_bay_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.mossel_bay_alt_tenders import MosselBayAltSource
    src = MosselBayAltSource()
    assert src.source_id == "mossel_bay_alt_tenders"
    assert src.live is True


def test_mossel_bay_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.mossel_bay_alt_tenders import MosselBayAltSource, MOCK_HTML
    src = MosselBayAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mossel_bay_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.mossel_bay_alt_tenders import MosselBayAltSource
    src = MosselBayAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
