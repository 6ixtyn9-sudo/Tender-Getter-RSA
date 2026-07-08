"""Tests for the Buffalo City TVET College tender source plug-in."""
import pytest


def test_buffalo_city_tvet_source_initialization():
    from tender_getter.sources.tvet.buffalo_city_tvet import BuffaloCityTvetSource
    src = BuffaloCityTvetSource()
    assert src.source_id == "buffalo_city_tvet"
    assert src.live is True


def test_buffalo_city_tvet_parse_mock_html():
    from tender_getter.sources.tvet.buffalo_city_tvet import BuffaloCityTvetSource, MOCK_HTML
    src = BuffaloCityTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_buffalo_city_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.buffalo_city_tvet import BuffaloCityTvetSource
    src = BuffaloCityTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
