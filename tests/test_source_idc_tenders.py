"""Tests for the Industrial Development Corporation tender source plug-in."""
import pytest


def test_idc_tenders_source_initialization():
    from tender_getter.sources.research_extra.idc_tenders import IdcSource
    src = IdcSource()
    assert src.source_id == "idc_tenders"
    assert src.live is True


def test_idc_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.idc_tenders import IdcSource, MOCK_HTML
    src = IdcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_idc_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.idc_tenders import IdcSource
    src = IdcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
