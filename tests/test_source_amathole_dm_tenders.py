"""Tests for the Amathole District Municipality tender source plug-in."""
import pytest


def test_amathole_dm_tenders_source_initialization():
    from tender_getter.sources.districts_full.amathole_dm_tenders import AmatholeDmSource
    src = AmatholeDmSource()
    assert src.source_id == "amathole_dm_tenders"
    assert src.live is True


def test_amathole_dm_tenders_parse_mock_html():
    from tender_getter.sources.districts_full.amathole_dm_tenders import AmatholeDmSource, MOCK_HTML
    src = AmatholeDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_amathole_dm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts_full.amathole_dm_tenders import AmatholeDmSource
    src = AmatholeDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
