"""Tests for the Gauteng Department of Roads and Transport tender source plug-in."""
import pytest


def test_gdrt_tenders_source_initialization():
    from tender_getter.sources.research_extra.gdrt_tenders import GdrtSource
    src = GdrtSource()
    assert src.source_id == "gdrt_tenders"
    assert src.live is True


def test_gdrt_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.gdrt_tenders import GdrtSource, MOCK_HTML
    src = GdrtSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gdrt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.gdrt_tenders import GdrtSource
    src = GdrtSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
