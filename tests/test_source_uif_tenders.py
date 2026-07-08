"""Tests for the Unemployment Insurance Fund tender source plug-in."""
import pytest


def test_uif_tenders_source_initialization():
    from tender_getter.sources.research_extra.uif_tenders import UifSource
    src = UifSource()
    assert src.source_id == "uif_tenders"
    assert src.live is True


def test_uif_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.uif_tenders import UifSource, MOCK_HTML
    src = UifSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_uif_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.uif_tenders import UifSource
    src = UifSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
