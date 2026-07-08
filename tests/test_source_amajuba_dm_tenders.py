"""Tests for the Amajuba District Municipality tender source plug-in."""
import pytest


def test_amajuba_dm_tenders_source_initialization():
    from tender_getter.sources.districts_full.amajuba_dm_tenders import AmajubaDmSource
    src = AmajubaDmSource()
    assert src.source_id == "amajuba_dm_tenders"
    assert src.live is True


def test_amajuba_dm_tenders_parse_mock_html():
    from tender_getter.sources.districts_full.amajuba_dm_tenders import AmajubaDmSource, MOCK_HTML
    src = AmajubaDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_amajuba_dm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts_full.amajuba_dm_tenders import AmajubaDmSource
    src = AmajubaDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
