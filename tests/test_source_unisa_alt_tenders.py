"""Tests for the UNISA (alt) tender source plug-in."""
import pytest


def test_unisa_alt_tenders_source_initialization():
    from tender_getter.sources.universities.unisa_alt_tenders import UnisaAltSource
    src = UnisaAltSource()
    assert src.source_id == "unisa_alt_tenders"
    assert src.live is True


def test_unisa_alt_tenders_parse_mock_html():
    from tender_getter.sources.universities.unisa_alt_tenders import UnisaAltSource, MOCK_HTML
    src = UnisaAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_unisa_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.unisa_alt_tenders import UnisaAltSource
    src = UnisaAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
