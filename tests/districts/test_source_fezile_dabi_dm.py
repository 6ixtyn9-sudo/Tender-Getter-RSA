"""Tests for the Fezile Dabi District Municipality tender source plug-in."""
import pytest


def test_fezile_dabi_dm_source_initialization():
    from tender_getter.sources.districts.fezile_dabi_dm import FezileDabiDmSource
    src = FezileDabiDmSource()
    assert src.source_id == "fezile_dabi_dm"
    assert src.live is True


def test_fezile_dabi_dm_parse_mock_html():
    from tender_getter.sources.districts.fezile_dabi_dm import FezileDabiDmSource, MOCK_HTML
    src = FezileDabiDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fezile_dabi_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.fezile_dabi_dm import FezileDabiDmSource
    src = FezileDabiDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
