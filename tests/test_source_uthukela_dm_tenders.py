"""Tests for the uThukela District Municipality tender source plug-in."""
import pytest


def test_uthukela_dm_tenders_source_initialization():
    from tender_getter.sources.districts_full.uthukela_dm_tenders import UthukelaDmSource
    src = UthukelaDmSource()
    assert src.source_id == "uthukela_dm_tenders"
    assert src.live is True


def test_uthukela_dm_tenders_parse_mock_html():
    from tender_getter.sources.districts_full.uthukela_dm_tenders import UthukelaDmSource, MOCK_HTML
    src = UthukelaDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_uthukela_dm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts_full.uthukela_dm_tenders import UthukelaDmSource
    src = UthukelaDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
