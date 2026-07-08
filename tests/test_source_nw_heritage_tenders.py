"""Tests for the North West Heritage Foundation tender source plug-in."""
import pytest


def test_nw_heritage_tenders_source_initialization():
    from tender_getter.sources.research_extra.nw_heritage_tenders import NwHeritageSource
    src = NwHeritageSource()
    assert src.source_id == "nw_heritage_tenders"
    assert src.live is False


def test_nw_heritage_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.nw_heritage_tenders import NwHeritageSource, MOCK_HTML
    src = NwHeritageSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nw_heritage_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.nw_heritage_tenders import NwHeritageSource
    src = NwHeritageSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
