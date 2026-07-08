"""Tests for the Gauteng Department of Infrastructure Development tender source plug-in."""
import pytest


def test_gdid_tenders_source_initialization():
    from tender_getter.sources.research_extra.gdid_tenders import GdidSource
    src = GdidSource()
    assert src.source_id == "gdid_tenders"
    assert src.live is True


def test_gdid_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.gdid_tenders import GdidSource, MOCK_HTML
    src = GdidSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gdid_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.gdid_tenders import GdidSource
    src = GdidSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
