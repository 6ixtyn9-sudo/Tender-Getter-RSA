"""Tests for the Department of Defence tender source plug-in."""
import pytest


def test_dod_tenders_source_initialization():
    from tender_getter.sources.research_extra.dod_tenders import DodSource
    src = DodSource()
    assert src.source_id == "dod_tenders"
    assert src.live is True


def test_dod_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.dod_tenders import DodSource, MOCK_HTML
    src = DodSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dod_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.dod_tenders import DodSource
    src = DodSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
