"""Tests for the NECSA (alt) tender source plug-in."""
import pytest


def test_necsa_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.necsa_alt_tenders import NecsaAltSource
    src = NecsaAltSource()
    assert src.source_id == "necsa_alt_tenders"
    assert src.live is True


def test_necsa_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.necsa_alt_tenders import NecsaAltSource, MOCK_HTML
    src = NecsaAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_necsa_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.necsa_alt_tenders import NecsaAltSource
    src = NecsaAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
