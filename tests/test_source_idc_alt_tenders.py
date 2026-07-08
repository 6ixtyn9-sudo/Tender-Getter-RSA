"""Tests for the IDC (alt) tender source plug-in."""
import pytest


def test_idc_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.idc_alt_tenders import IdcAltSource
    src = IdcAltSource()
    assert src.source_id == "idc_alt_tenders"
    assert src.live is True


def test_idc_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.idc_alt_tenders import IdcAltSource, MOCK_HTML
    src = IdcAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_idc_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.idc_alt_tenders import IdcAltSource
    src = IdcAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
