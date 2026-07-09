"""Tests for the Mopani District Municipality tender source plug-in."""
import pytest


def test_mopani_dm_source_initialization():
    from tender_getter.sources.districts.mopani_dm import MopaniDmSource
    src = MopaniDmSource()
    assert src.source_id == "mopani_dm"
    assert isinstance(src.live, bool)


def test_mopani_dm_parse_mock_html():
    from tender_getter.sources.districts.mopani_dm import MopaniDmSource, MOCK_HTML
    src = MopaniDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mopani_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.mopani_dm import MopaniDmSource
    src = MopaniDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
