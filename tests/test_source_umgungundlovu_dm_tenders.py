"""Tests for the uMgungundlovu District Municipality tender source plug-in."""
import pytest


def test_umgungundlovu_dm_tenders_source_initialization():
    from tender_getter.sources.districts_full.umgungundlovu_dm_tenders import UmgungundlovuDmSource
    src = UmgungundlovuDmSource()
    assert src.source_id == "umgungundlovu_dm_tenders"
    assert src.live is True


def test_umgungundlovu_dm_tenders_parse_mock_html():
    from tender_getter.sources.districts_full.umgungundlovu_dm_tenders import UmgungundlovuDmSource, MOCK_HTML
    src = UmgungundlovuDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umgungundlovu_dm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts_full.umgungundlovu_dm_tenders import UmgungundlovuDmSource
    src = UmgungundlovuDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
