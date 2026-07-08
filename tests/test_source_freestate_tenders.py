"""Tests for the Free State Provincial Treasury tender source plug-in."""
import pytest


def test_freestate_tenders_source_initialization():
    from tender_getter.sources.research_extra.freestate_tenders import FreestateSource
    src = FreestateSource()
    assert src.source_id == "freestate_tenders"
    assert src.live is True


def test_freestate_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.freestate_tenders import FreestateSource, MOCK_HTML
    src = FreestateSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_freestate_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.freestate_tenders import FreestateSource
    src = FreestateSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
