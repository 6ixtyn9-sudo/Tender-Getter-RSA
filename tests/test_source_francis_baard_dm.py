"""Tests for the Francis Baard District Municipality tender source plug-in."""
import pytest


def test_francis_baard_dm_source_initialization():
    from tender_getter.sources.districts.francis_baard_dm import FrancisBaardDmSource
    src = FrancisBaardDmSource()
    assert src.source_id == "francis_baard_dm"
    assert src.live is True


def test_francis_baard_dm_parse_mock_html():
    from tender_getter.sources.districts.francis_baard_dm import FrancisBaardDmSource, MOCK_HTML
    src = FrancisBaardDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_francis_baard_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.francis_baard_dm import FrancisBaardDmSource
    src = FrancisBaardDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
