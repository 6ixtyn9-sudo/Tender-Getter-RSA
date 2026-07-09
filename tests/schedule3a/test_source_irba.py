"""Tests for the Independent Regulatory Board for Auditors (IRBA) tender source plug-in."""
import pytest


def test_irba_source_initialization():
    from tender_getter.sources.schedule3a.irba import IrbaSource
    src = IrbaSource()
    assert src.source_id == "irba"
    assert isinstance(src.live, bool)


def test_irba_parse_mock_html():
    from tender_getter.sources.schedule3a.irba import IrbaSource, MOCK_HTML
    src = IrbaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_irba_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.irba import IrbaSource
    src = IrbaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
