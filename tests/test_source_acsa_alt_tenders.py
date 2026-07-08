"""Tests for the ACSA (alt) tender source plug-in."""
import pytest


def test_acsa_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.acsa_alt_tenders import AcsaAltSource
    src = AcsaAltSource()
    assert src.source_id == "acsa_alt_tenders"
    assert src.live is True


def test_acsa_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.acsa_alt_tenders import AcsaAltSource, MOCK_HTML
    src = AcsaAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_acsa_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.acsa_alt_tenders import AcsaAltSource
    src = AcsaAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
