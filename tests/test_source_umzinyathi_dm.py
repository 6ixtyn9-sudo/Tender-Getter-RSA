"""Tests for the uMzinyathi District Municipality tender source plug-in."""
import pytest


def test_umzinyathi_dm_source_initialization():
    from tender_getter.sources.districts.umzinyathi_dm import UmzinyathiDmSource
    src = UmzinyathiDmSource()
    assert src.source_id == "umzinyathi_dm"
    assert src.live is True


def test_umzinyathi_dm_parse_mock_html():
    from tender_getter.sources.districts.umzinyathi_dm import UmzinyathiDmSource, MOCK_HTML
    src = UmzinyathiDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umzinyathi_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.umzinyathi_dm import UmzinyathiDmSource
    src = UmzinyathiDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
