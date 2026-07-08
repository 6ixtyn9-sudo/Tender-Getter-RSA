"""Tests for the Namakwa District Municipality tender source plug-in."""
import pytest


def test_namakwa_dm_tenders_source_initialization():
    from tender_getter.sources.districts_full.namakwa_dm_tenders import NamakwaDmSource
    src = NamakwaDmSource()
    assert src.source_id == "namakwa_dm_tenders"
    assert src.live is True


def test_namakwa_dm_tenders_parse_mock_html():
    from tender_getter.sources.districts_full.namakwa_dm_tenders import NamakwaDmSource, MOCK_HTML
    src = NamakwaDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_namakwa_dm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts_full.namakwa_dm_tenders import NamakwaDmSource
    src = NamakwaDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
