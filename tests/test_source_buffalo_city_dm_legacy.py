"""Tests for the Buffalo City (legacy DM code) tender source plug-in."""
import pytest


def test_buffalo_city_dm_legacy_source_initialization():
    from tender_getter.sources.districts.buffalo_city_dm_legacy import BuffaloCityDmLegacySource
    src = BuffaloCityDmLegacySource()
    assert src.source_id == "buffalo_city_dm_legacy"
    assert src.live is False


def test_buffalo_city_dm_legacy_parse_mock_html():
    from tender_getter.sources.districts.buffalo_city_dm_legacy import BuffaloCityDmLegacySource, MOCK_HTML
    src = BuffaloCityDmLegacySource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_buffalo_city_dm_legacy_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.buffalo_city_dm_legacy import BuffaloCityDmLegacySource
    src = BuffaloCityDmLegacySource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
