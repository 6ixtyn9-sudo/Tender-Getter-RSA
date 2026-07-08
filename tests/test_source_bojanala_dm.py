"""Tests for the Bojanala District Municipality tender source plug-in."""
import pytest


def test_bojanala_dm_source_initialization():
    from tender_getter.sources.districts.bojanala_dm import BojanalaDmSource
    src = BojanalaDmSource()
    assert src.source_id == "bojanala_dm"
    assert src.live is True


def test_bojanala_dm_parse_mock_html():
    from tender_getter.sources.districts.bojanala_dm import BojanalaDmSource, MOCK_HTML
    src = BojanalaDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_bojanala_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.bojanala_dm import BojanalaDmSource
    src = BojanalaDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
