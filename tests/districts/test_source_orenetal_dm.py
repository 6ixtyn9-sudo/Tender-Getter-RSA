"""Tests for the OR Tambo (DM-form legacy) tender source plug-in."""
import pytest


def test_orenetal_dm_source_initialization():
    from tender_getter.sources.districts.orenetal_dm import OrenetalDmSource
    src = OrenetalDmSource()
    assert src.source_id == "orenetal_dm"
    assert src.live is False


def test_orenetal_dm_parse_mock_html():
    from tender_getter.sources.districts.orenetal_dm import OrenetalDmSource, MOCK_HTML
    src = OrenetalDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_orenetal_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.orenetal_dm import OrenetalDmSource
    src = OrenetalDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
