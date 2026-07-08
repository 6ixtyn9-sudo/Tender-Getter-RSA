"""Tests for the Free State Development Corporation (FDC) tender source plug-in."""
import pytest


def test_fdc_tenders_source_initialization():
    from tender_getter.sources.research_extra.fdc_tenders import FdcSource
    src = FdcSource()
    assert src.source_id == "fdc_tenders"
    assert src.live is False


def test_fdc_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.fdc_tenders import FdcSource, MOCK_HTML
    src = FdcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fdc_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.fdc_tenders import FdcSource
    src = FdcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
