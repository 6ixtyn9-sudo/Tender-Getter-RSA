"""Tests for the Department of Basic Education tender source plug-in."""
import pytest


def test_dbe_tenders_source_initialization():
    from tender_getter.sources.research_extra.dbe_tenders import DbeSource
    src = DbeSource()
    assert src.source_id == "dbe_tenders"
    assert src.live is True


def test_dbe_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.dbe_tenders import DbeSource, MOCK_HTML
    src = DbeSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dbe_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.dbe_tenders import DbeSource
    src = DbeSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
