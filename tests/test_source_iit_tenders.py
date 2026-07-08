"""Tests for the Independent Institute of Technology tender source plug-in."""
import pytest


def test_iit_tenders_source_initialization():
    from tender_getter.sources.research_extra.iit_tenders import IitSource
    src = IitSource()
    assert src.source_id == "iit_tenders"
    assert src.live is False


def test_iit_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.iit_tenders import IitSource, MOCK_HTML
    src = IitSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_iit_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.iit_tenders import IitSource
    src = IitSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
