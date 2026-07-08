"""Tests for the Cape Winelands District Municipality tender source plug-in."""
import pytest


def test_cape_winelands_tenders_source_initialization():
    from tender_getter.sources.research_extra.cape_winelands_tenders import CapeWinelandsSource
    src = CapeWinelandsSource()
    assert src.source_id == "cape_winelands_tenders"
    assert src.live is True


def test_cape_winelands_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.cape_winelands_tenders import CapeWinelandsSource, MOCK_HTML
    src = CapeWinelandsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_cape_winelands_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.cape_winelands_tenders import CapeWinelandsSource
    src = CapeWinelandsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
