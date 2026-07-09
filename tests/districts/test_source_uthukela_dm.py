"""Tests for the uThukela District Municipality tender source plug-in."""
import pytest


def test_uthukela_dm_source_initialization():
    from tender_getter.sources.districts.uthukela_dm import UthukelaDmSource
    src = UthukelaDmSource()
    assert src.source_id == "uthukela_dm"
    assert isinstance(src.live, bool)


def test_uthukela_dm_parse_mock_html():
    from tender_getter.sources.districts.uthukela_dm import UthukelaDmSource, MOCK_HTML
    src = UthukelaDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_uthukela_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.uthukela_dm import UthukelaDmSource
    src = UthukelaDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
