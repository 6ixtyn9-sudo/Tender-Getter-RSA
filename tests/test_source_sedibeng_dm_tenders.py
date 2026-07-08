"""Tests for the Sedibeng District Municipality tender source plug-in."""
import pytest


def test_sedibeng_dm_tenders_source_initialization():
    from tender_getter.sources.research_extra.sedibeng_dm_tenders import SedibengDmSource
    src = SedibengDmSource()
    assert src.source_id == "sedibeng_dm_tenders"
    assert src.live is True


def test_sedibeng_dm_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.sedibeng_dm_tenders import SedibengDmSource, MOCK_HTML
    src = SedibengDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sedibeng_dm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.sedibeng_dm_tenders import SedibengDmSource
    src = SedibengDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
