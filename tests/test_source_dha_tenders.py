"""Tests for the Department of Home Affairs tender source plug-in."""
import pytest


def test_dha_tenders_source_initialization():
    from tender_getter.sources.research_extra.dha_tenders import DhaSource
    src = DhaSource()
    assert src.source_id == "dha_tenders"
    assert src.live is True


def test_dha_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.dha_tenders import DhaSource, MOCK_HTML
    src = DhaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dha_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.dha_tenders import DhaSource
    src = DhaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
