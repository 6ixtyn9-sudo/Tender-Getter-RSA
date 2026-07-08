"""Tests for the Mine Health and Safety Council (MHSC) tender source plug-in."""
import pytest


def test_mhsc_tenders_source_initialization():
    from tender_getter.sources.schedule3a.mhsc_tenders import MhscSource
    src = MhscSource()
    assert src.source_id == "mhsc_tenders"
    assert src.live is True


def test_mhsc_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.mhsc_tenders import MhscSource, MOCK_HTML
    src = MhscSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mhsc_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.mhsc_tenders import MhscSource
    src = MhscSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
