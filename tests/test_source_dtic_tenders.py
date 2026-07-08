"""Tests for the Department of Trade, Industry & Competition tender source plug-in."""
import pytest


def test_dtic_tenders_source_initialization():
    from tender_getter.sources.research_extra.dtic_tenders import DticSource
    src = DticSource()
    assert src.source_id == "dtic_tenders"
    assert src.live is True


def test_dtic_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.dtic_tenders import DticSource, MOCK_HTML
    src = DticSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dtic_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.dtic_tenders import DticSource
    src = DticSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
