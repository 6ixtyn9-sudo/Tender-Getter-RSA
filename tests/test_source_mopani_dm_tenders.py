"""Tests for the Mopani District Municipality tender source plug-in."""
import pytest


def test_mopani_dm_tenders_source_initialization():
    from tender_getter.sources.districts_full.mopani_dm_tenders import MopaniDmSource
    src = MopaniDmSource()
    assert src.source_id == "mopani_dm_tenders"
    assert src.live is True


def test_mopani_dm_tenders_parse_mock_html():
    from tender_getter.sources.districts_full.mopani_dm_tenders import MopaniDmSource, MOCK_HTML
    src = MopaniDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mopani_dm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts_full.mopani_dm_tenders import MopaniDmSource
    src = MopaniDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
