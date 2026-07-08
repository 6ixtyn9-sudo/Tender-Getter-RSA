"""Tests for the Office of the Chief Justice (OCJ) tender source plug-in."""
import pytest


def test_ocj_tenders_source_initialization():
    from tender_getter.sources.schedule3a.ocj_tenders import OcjSource
    src = OcjSource()
    assert src.source_id == "ocj_tenders"
    assert src.live is True


def test_ocj_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.ocj_tenders import OcjSource, MOCK_HTML
    src = OcjSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ocj_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.ocj_tenders import OcjSource
    src = OcjSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
