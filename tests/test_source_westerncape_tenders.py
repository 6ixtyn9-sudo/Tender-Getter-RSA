"""Tests for the Western Cape Government Tenders tender source plug-in."""
import pytest


def test_westerncape_tenders_source_initialization():
    from tender_getter.sources.research_extra.westerncape_tenders import WesterncapeSource
    src = WesterncapeSource()
    assert src.source_id == "westerncape_tenders"
    assert src.live is True


def test_westerncape_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.westerncape_tenders import WesterncapeSource, MOCK_HTML
    src = WesterncapeSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_westerncape_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.westerncape_tenders import WesterncapeSource
    src = WesterncapeSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
