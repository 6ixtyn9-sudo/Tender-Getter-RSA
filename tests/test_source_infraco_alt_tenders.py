"""Tests for the Infraco (alt) tender source plug-in."""
import pytest


def test_infraco_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.infraco_alt_tenders import InfracoAltSource
    src = InfracoAltSource()
    assert src.source_id == "infraco_alt_tenders"
    assert src.live is True


def test_infraco_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.infraco_alt_tenders import InfracoAltSource, MOCK_HTML
    src = InfracoAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_infraco_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.infraco_alt_tenders import InfracoAltSource
    src = InfracoAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
