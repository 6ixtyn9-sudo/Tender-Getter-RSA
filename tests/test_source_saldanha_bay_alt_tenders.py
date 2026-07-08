"""Tests for the Saldanha Bay (alt) tender source plug-in."""
import pytest


def test_saldanha_bay_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.saldanha_bay_alt_tenders import SaldanhaBayAltSource
    src = SaldanhaBayAltSource()
    assert src.source_id == "saldanha_bay_alt_tenders"
    assert src.live is True


def test_saldanha_bay_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.saldanha_bay_alt_tenders import SaldanhaBayAltSource, MOCK_HTML
    src = SaldanhaBayAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_saldanha_bay_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.saldanha_bay_alt_tenders import SaldanhaBayAltSource
    src = SaldanhaBayAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
