"""Tests for the South African Nuclear Energy Corporation tender source plug-in."""
import pytest


def test_necsa_tenders_source_initialization():
    from tender_getter.sources.research_extra.necsa_tenders import NecsaSource
    src = NecsaSource()
    assert src.source_id == "necsa_tenders"
    assert src.live is True


def test_necsa_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.necsa_tenders import NecsaSource, MOCK_HTML
    src = NecsaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_necsa_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.necsa_tenders import NecsaSource
    src = NecsaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
