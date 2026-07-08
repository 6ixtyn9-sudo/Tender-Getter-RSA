"""Tests for the sefa (alt) tender source plug-in."""
import pytest


def test_sefa_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.sefa_alt_tenders import SefaAltSource
    src = SefaAltSource()
    assert src.source_id == "sefa_alt_tenders"
    assert src.live is True


def test_sefa_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.sefa_alt_tenders import SefaAltSource, MOCK_HTML
    src = SefaAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sefa_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.sefa_alt_tenders import SefaAltSource
    src = SefaAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
