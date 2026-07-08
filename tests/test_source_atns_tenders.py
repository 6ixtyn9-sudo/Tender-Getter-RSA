"""Tests for the Air Traffic & Navigation Services tender source plug-in."""
import pytest


def test_atns_tenders_source_initialization():
    from tender_getter.sources.research_extra.atns_tenders import AtnsSource
    src = AtnsSource()
    assert src.source_id == "atns_tenders"
    assert src.live is True


def test_atns_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.atns_tenders import AtnsSource, MOCK_HTML
    src = AtnsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_atns_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.atns_tenders import AtnsSource
    src = AtnsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
