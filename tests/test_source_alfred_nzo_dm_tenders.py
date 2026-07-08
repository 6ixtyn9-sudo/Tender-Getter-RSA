"""Tests for the Alfred Nzo District Municipality tender source plug-in."""
import pytest


def test_alfred_nzo_dm_tenders_source_initialization():
    from tender_getter.sources.districts_full.alfred_nzo_dm_tenders import AlfredNzoDmSource
    src = AlfredNzoDmSource()
    assert src.source_id == "alfred_nzo_dm_tenders"
    assert src.live is True


def test_alfred_nzo_dm_tenders_parse_mock_html():
    from tender_getter.sources.districts_full.alfred_nzo_dm_tenders import AlfredNzoDmSource, MOCK_HTML
    src = AlfredNzoDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_alfred_nzo_dm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts_full.alfred_nzo_dm_tenders import AlfredNzoDmSource
    src = AlfredNzoDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
