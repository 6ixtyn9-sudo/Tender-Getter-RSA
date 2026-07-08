"""Tests for the Harry Gwala District Municipality tender source plug-in."""
import pytest


def test_harry_gwala_dm_source_initialization():
    from tender_getter.sources.districts.harry_gwala_dm import HarryGwalaDmSource
    src = HarryGwalaDmSource()
    assert src.source_id == "harry_gwala_dm"
    assert src.live is True


def test_harry_gwala_dm_parse_mock_html():
    from tender_getter.sources.districts.harry_gwala_dm import HarryGwalaDmSource, MOCK_HTML
    src = HarryGwalaDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_harry_gwala_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.harry_gwala_dm import HarryGwalaDmSource
    src = HarryGwalaDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
