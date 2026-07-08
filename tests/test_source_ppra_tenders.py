"""Tests for the Property Practitioners Regulatory Authority (PPRA) tender source plug-in."""
import pytest


def test_ppra_tenders_source_initialization():
    from tender_getter.sources.schedule3a.ppra_tenders import PpraSource
    src = PpraSource()
    assert src.source_id == "ppra_tenders"
    assert src.live is True


def test_ppra_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.ppra_tenders import PpraSource, MOCK_HTML
    src = PpraSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ppra_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.ppra_tenders import PpraSource
    src = PpraSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
