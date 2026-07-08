"""Tests for the National School of Government (NSG) tender source plug-in."""
import pytest


def test_nsg_tenders_source_initialization():
    from tender_getter.sources.schedule3a.nsg_tenders import NsgSource
    src = NsgSource()
    assert src.source_id == "nsg_tenders"
    assert src.live is True


def test_nsg_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.nsg_tenders import NsgSource, MOCK_HTML
    src = NsgSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nsg_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.nsg_tenders import NsgSource
    src = NsgSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
