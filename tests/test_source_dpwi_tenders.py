"""Tests for the Department of Public Works & Infrastructure tender source plug-in."""
import pytest


def test_dpwi_tenders_source_initialization():
    from tender_getter.sources.research_extra.dpwi_tenders import DpwiSource
    src = DpwiSource()
    assert src.source_id == "dpwi_tenders"
    assert src.live is True


def test_dpwi_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.dpwi_tenders import DpwiSource, MOCK_HTML
    src = DpwiSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dpwi_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.dpwi_tenders import DpwiSource
    src = DpwiSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
