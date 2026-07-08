"""Tests for the Department of Sports, Arts & Culture tender source plug-in."""
import pytest


def test_dsac_tenders_source_initialization():
    from tender_getter.sources.research_extra.dsac_tenders import DsacSource
    src = DsacSource()
    assert src.source_id == "dsac_tenders"
    assert src.live is True


def test_dsac_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.dsac_tenders import DsacSource, MOCK_HTML
    src = DsacSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dsac_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.dsac_tenders import DsacSource
    src = DsacSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
