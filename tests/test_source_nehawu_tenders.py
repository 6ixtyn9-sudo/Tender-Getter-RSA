"""Tests for the NEHAWU tender source plug-in."""
import pytest


def test_nehawu_tenders_source_initialization():
    from tender_getter.sources.research_extra.nehawu_tenders import NehawuSource
    src = NehawuSource()
    assert src.source_id == "nehawu_tenders"
    assert src.live is False


def test_nehawu_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.nehawu_tenders import NehawuSource, MOCK_HTML
    src = NehawuSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nehawu_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.nehawu_tenders import NehawuSource
    src = NehawuSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
