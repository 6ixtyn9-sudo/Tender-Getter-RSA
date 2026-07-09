"""Tests for the Central Karoo District Municipality tender source plug-in."""
import pytest


def test_central_karoo_dm_source_initialization():
    from tender_getter.sources.districts.central_karoo_dm import CentralKarooDmSource
    src = CentralKarooDmSource()
    assert src.source_id == "central_karoo_dm"
    assert isinstance(src.live, bool)


def test_central_karoo_dm_parse_mock_html():
    from tender_getter.sources.districts.central_karoo_dm import CentralKarooDmSource, MOCK_HTML
    src = CentralKarooDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_central_karoo_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.central_karoo_dm import CentralKarooDmSource
    src = CentralKarooDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
