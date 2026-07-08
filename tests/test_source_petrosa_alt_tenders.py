"""Tests for the PetroSA (alt) tender source plug-in."""
import pytest


def test_petrosa_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.petrosa_alt_tenders import PetrosaAltSource
    src = PetrosaAltSource()
    assert src.source_id == "petrosa_alt_tenders"
    assert src.live is True


def test_petrosa_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.petrosa_alt_tenders import PetrosaAltSource, MOCK_HTML
    src = PetrosaAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_petrosa_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.petrosa_alt_tenders import PetrosaAltSource
    src = PetrosaAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
