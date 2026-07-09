"""Tests for the Free State Development Corporation (FDC) tender source plug-in."""
import pytest


def test_fdc_source_initialization():
    from tender_getter.sources.research.fdc import FdcSource
    src = FdcSource()
    assert src.source_id == "fdc"
    assert isinstance(src.live, bool)


def test_fdc_parse_mock_html():
    from tender_getter.sources.research.fdc import FdcSource, MOCK_HTML
    src = FdcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fdc_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.fdc import FdcSource
    src = FdcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
