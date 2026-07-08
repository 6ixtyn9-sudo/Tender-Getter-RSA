"""Tests for the SA Power Pool Operations tender source plug-in."""
import pytest


def test_sapower_tenders_source_initialization():
    from tender_getter.sources.research_extra.sapower_tenders import SapowerSource
    src = SapowerSource()
    assert src.source_id == "sapower_tenders"
    assert src.live is False


def test_sapower_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.sapower_tenders import SapowerSource, MOCK_HTML
    src = SapowerSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sapower_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.sapower_tenders import SapowerSource
    src = SapowerSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
