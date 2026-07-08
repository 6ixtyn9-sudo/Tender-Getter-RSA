"""Tests for the UIF (alt) tender source plug-in."""
import pytest


def test_uif_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.uif_alt_tenders import UifAltSource
    src = UifAltSource()
    assert src.source_id == "uif_alt_tenders"
    assert src.live is True


def test_uif_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.uif_alt_tenders import UifAltSource, MOCK_HTML
    src = UifAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_uif_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.uif_alt_tenders import UifAltSource
    src = UifAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
