"""Tests for the Buffalo City Metropolitan Municipality tender source plug-in."""
import pytest


def test_buffalo_city_tenders_source_initialization():
    from tender_getter.sources.research_extra.buffalo_city_tenders import BuffaloCitySource
    src = BuffaloCitySource()
    assert src.source_id == "buffalo_city_tenders"
    assert src.live is True


def test_buffalo_city_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.buffalo_city_tenders import BuffaloCitySource, MOCK_HTML
    src = BuffaloCitySource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_buffalo_city_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.buffalo_city_tenders import BuffaloCitySource
    src = BuffaloCitySource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
