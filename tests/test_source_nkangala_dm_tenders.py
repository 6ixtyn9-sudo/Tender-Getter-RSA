"""Tests for the Nkangala District Municipality tender source plug-in."""
import pytest


def test_nkangala_dm_tenders_source_initialization():
    from tender_getter.sources.districts_full.nkangala_dm_tenders import NkangalaDmSource
    src = NkangalaDmSource()
    assert src.source_id == "nkangala_dm_tenders"
    assert src.live is True


def test_nkangala_dm_tenders_parse_mock_html():
    from tender_getter.sources.districts_full.nkangala_dm_tenders import NkangalaDmSource, MOCK_HTML
    src = NkangalaDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nkangala_dm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts_full.nkangala_dm_tenders import NkangalaDmSource
    src = NkangalaDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
