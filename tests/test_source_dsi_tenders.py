"""Tests for the Department of Science & Innovation tender source plug-in."""
import pytest


def test_dsi_tenders_source_initialization():
    from tender_getter.sources.research_extra.dsi_tenders import DsiSource
    src = DsiSource()
    assert src.source_id == "dsi_tenders"
    assert src.live is True


def test_dsi_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.dsi_tenders import DsiSource, MOCK_HTML
    src = DsiSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dsi_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.dsi_tenders import DsiSource
    src = DsiSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
