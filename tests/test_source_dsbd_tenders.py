"""Tests for the Department of Small Business Development tender source plug-in."""
import pytest


def test_dsbd_tenders_source_initialization():
    from tender_getter.sources.research_extra.dsbd_tenders import DsbdSource
    src = DsbdSource()
    assert src.source_id == "dsbd_tenders"
    assert src.live is True


def test_dsbd_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.dsbd_tenders import DsbdSource, MOCK_HTML
    src = DsbdSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dsbd_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.dsbd_tenders import DsbdSource
    src = DsbdSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
