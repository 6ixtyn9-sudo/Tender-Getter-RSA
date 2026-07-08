"""Tests for the DPME (alt URL) tender source plug-in."""
import pytest


def test_dpm_e_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.dpm_e_alt_tenders import DpmEAltSource
    src = DpmEAltSource()
    assert src.source_id == "dpm_e_alt_tenders"
    assert src.live is True


def test_dpm_e_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.dpm_e_alt_tenders import DpmEAltSource, MOCK_HTML
    src = DpmEAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dpm_e_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.dpm_e_alt_tenders import DpmEAltSource
    src = DpmEAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
