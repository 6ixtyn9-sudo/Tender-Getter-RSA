"""Tests for the CSOS (alt) tender source plug-in."""
import pytest


def test_csos_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.csos_alt_tenders import CsosAltSource
    src = CsosAltSource()
    assert src.source_id == "csos_alt_tenders"
    assert src.live is True


def test_csos_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.csos_alt_tenders import CsosAltSource, MOCK_HTML
    src = CsosAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_csos_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.csos_alt_tenders import CsosAltSource
    src = CsosAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
