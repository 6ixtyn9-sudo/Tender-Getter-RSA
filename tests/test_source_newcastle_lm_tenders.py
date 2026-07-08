"""Tests for the Newcastle Local Municipality tender source plug-in."""
import pytest


def test_newcastle_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.newcastle_lm_tenders import NewcastleLmSource
    src = NewcastleLmSource()
    assert src.source_id == "newcastle_lm_tenders"
    assert src.live is True


def test_newcastle_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.newcastle_lm_tenders import NewcastleLmSource, MOCK_HTML
    src = NewcastleLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_newcastle_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.newcastle_lm_tenders import NewcastleLmSource
    src = NewcastleLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
