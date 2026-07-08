"""Tests for the Zululand District Municipality tender source plug-in."""
import pytest


def test_zululand_dm_source_initialization():
    from tender_getter.sources.districts.zululand_dm import ZululandDmSource
    src = ZululandDmSource()
    assert src.source_id == "zululand_dm"
    assert src.live is True


def test_zululand_dm_parse_mock_html():
    from tender_getter.sources.districts.zululand_dm import ZululandDmSource, MOCK_HTML
    src = ZululandDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_zululand_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.zululand_dm import ZululandDmSource
    src = ZululandDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
