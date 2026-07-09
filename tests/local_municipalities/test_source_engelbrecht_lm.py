"""Tests for the Engelbrecht LM tender source plug-in."""
import pytest


def test_engelbrecht_lm_source_initialization():
    from tender_getter.sources.local_municipalities.engelbrecht_lm import EngelbrechtLmSource
    src = EngelbrechtLmSource()
    assert src.source_id == "engelbrecht_lm"
    assert isinstance(src.live, bool)


def test_engelbrecht_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.engelbrecht_lm import EngelbrechtLmSource, MOCK_HTML
    src = EngelbrechtLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_engelbrecht_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.engelbrecht_lm import EngelbrechtLmSource
    src = EngelbrechtLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
