"""Tests for the National Heritage Council (NHC) tender source plug-in."""
import pytest


def test_nhc_tenders_source_initialization():
    from tender_getter.sources.research_extra.nhc_tenders import NhcSource
    src = NhcSource()
    assert src.source_id == "nhc_tenders"
    assert src.live is True


def test_nhc_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.nhc_tenders import NhcSource, MOCK_HTML
    src = NhcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nhc_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.nhc_tenders import NhcSource
    src = NhcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
