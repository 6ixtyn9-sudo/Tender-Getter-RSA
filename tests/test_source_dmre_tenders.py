"""Tests for the Department of Mineral Resources & Energy tender source plug-in."""
import pytest


def test_dmre_tenders_source_initialization():
    from tender_getter.sources.research_extra.dmre_tenders import DmreSource
    src = DmreSource()
    assert src.source_id == "dmre_tenders"
    assert src.live is True


def test_dmre_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.dmre_tenders import DmreSource, MOCK_HTML
    src = DmreSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dmre_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.dmre_tenders import DmreSource
    src = DmreSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
