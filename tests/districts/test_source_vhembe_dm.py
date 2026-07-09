"""Tests for the Vhembe District Municipality tender source plug-in."""
import pytest


def test_vhembe_dm_source_initialization():
    from tender_getter.sources.districts.vhembe_dm import VhembeDmSource
    src = VhembeDmSource()
    assert src.source_id == "vhembe_dm"
    assert isinstance(src.live, bool)


def test_vhembe_dm_parse_mock_html():
    from tender_getter.sources.districts.vhembe_dm import VhembeDmSource, MOCK_HTML
    src = VhembeDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_vhembe_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.vhembe_dm import VhembeDmSource
    src = VhembeDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
