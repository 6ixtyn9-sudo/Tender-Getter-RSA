"""Tests for the Waterberg District Municipality tender source plug-in."""
import pytest


def test_waterberg_dm_source_initialization():
    from tender_getter.sources.districts.waterberg_dm import WaterbergDmSource
    src = WaterbergDmSource()
    assert src.source_id == "waterberg_dm"
    assert src.live is True


def test_waterberg_dm_parse_mock_html():
    from tender_getter.sources.districts.waterberg_dm import WaterbergDmSource, MOCK_HTML
    src = WaterbergDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_waterberg_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.waterberg_dm import WaterbergDmSource
    src = WaterbergDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
