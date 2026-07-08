"""Tests for the Thabo Mofutsanyana District Municipality tender source plug-in."""
import pytest


def test_thabo_mofutsanyana_dm_tenders_source_initialization():
    from tender_getter.sources.districts_full.thabo_mofutsanyana_dm_tenders import ThaboMofutsanyanaDmSource
    src = ThaboMofutsanyanaDmSource()
    assert src.source_id == "thabo_mofutsanyana_dm_tenders"
    assert src.live is True


def test_thabo_mofutsanyana_dm_tenders_parse_mock_html():
    from tender_getter.sources.districts_full.thabo_mofutsanyana_dm_tenders import ThaboMofutsanyanaDmSource, MOCK_HTML
    src = ThaboMofutsanyanaDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_thabo_mofutsanyana_dm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts_full.thabo_mofutsanyana_dm_tenders import ThaboMofutsanyanaDmSource
    src = ThaboMofutsanyanaDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
