"""Tests for the Property Practitioners Regulatory Authority (PPRA) tender source plug-in."""
import pytest


def test_ppra_source_initialization():
    from tender_getter.sources.regulators.ppra import PpraSource
    src = PpraSource()
    assert src.source_id == "ppra"
    assert src.live is True


def test_ppra_parse_mock_html():
    from tender_getter.sources.regulators.ppra import PpraSource, MOCK_HTML
    src = PpraSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ppra_fetch_uses_fallback_on_empty():
    from tender_getter.sources.regulators.ppra import PpraSource
    src = PpraSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
