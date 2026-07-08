"""Tests for the Transnet (alt) tender source plug-in."""
import pytest


def test_transnet_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.transnet_alt_tenders import TransnetAltSource
    src = TransnetAltSource()
    assert src.source_id == "transnet_alt_tenders"
    assert src.live is True


def test_transnet_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.transnet_alt_tenders import TransnetAltSource, MOCK_HTML
    src = TransnetAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_transnet_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.transnet_alt_tenders import TransnetAltSource
    src = TransnetAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
