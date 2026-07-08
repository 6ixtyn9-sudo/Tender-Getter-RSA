"""Tests for the Department of Correctional Services (alt URL) tender source plug-in."""
import pytest


def test_dcs_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.dcs_alt_tenders import DcsAltSource
    src = DcsAltSource()
    assert src.source_id == "dcs_alt_tenders"
    assert src.live is True


def test_dcs_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.dcs_alt_tenders import DcsAltSource, MOCK_HTML
    src = DcsAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dcs_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.dcs_alt_tenders import DcsAltSource
    src = DcsAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
