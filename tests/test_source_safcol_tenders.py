"""Tests for the South African Forestry Company tender source plug-in."""
import pytest


def test_safcol_tenders_source_initialization():
    from tender_getter.sources.research_extra.safcol_tenders import SafcolSource
    src = SafcolSource()
    assert src.source_id == "safcol_tenders"
    assert src.live is True


def test_safcol_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.safcol_tenders import SafcolSource, MOCK_HTML
    src = SafcolSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_safcol_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.safcol_tenders import SafcolSource
    src = SafcolSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
