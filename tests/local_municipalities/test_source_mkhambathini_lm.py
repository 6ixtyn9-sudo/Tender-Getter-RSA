"""Tests for the Mkhambathini LM tender source plug-in."""
import pytest


def test_mkhambathini_lm_source_initialization():
    from tender_getter.sources.local_municipalities.mkhambathini_lm import MkhambathiniLmSource
    src = MkhambathiniLmSource()
    assert src.source_id == "mkhambathini_lm"
    assert isinstance(src.live, bool)


def test_mkhambathini_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.mkhambathini_lm import MkhambathiniLmSource, MOCK_HTML
    src = MkhambathiniLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mkhambathini_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.mkhambathini_lm import MkhambathiniLmSource
    src = MkhambathiniLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
