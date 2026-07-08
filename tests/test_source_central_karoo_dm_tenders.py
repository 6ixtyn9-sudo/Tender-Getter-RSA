"""Tests for the Central Karoo District Municipality tender source plug-in."""
import pytest


def test_central_karoo_dm_tenders_source_initialization():
    from tender_getter.sources.districts_full.central_karoo_dm_tenders import CentralKarooDmSource
    src = CentralKarooDmSource()
    assert src.source_id == "central_karoo_dm_tenders"
    assert src.live is True


def test_central_karoo_dm_tenders_parse_mock_html():
    from tender_getter.sources.districts_full.central_karoo_dm_tenders import CentralKarooDmSource, MOCK_HTML
    src = CentralKarooDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_central_karoo_dm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts_full.central_karoo_dm_tenders import CentralKarooDmSource
    src = CentralKarooDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
