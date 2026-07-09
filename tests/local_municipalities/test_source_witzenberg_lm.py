"""Tests for the Witzenberg LM tender source plug-in."""
import pytest


def test_witzenberg_lm_source_initialization():
    from tender_getter.sources.local_municipalities.witzenberg_lm import WitzenbergLmSource
    src = WitzenbergLmSource()
    assert src.source_id == "witzenberg_lm"
    assert isinstance(src.live, bool)


def test_witzenberg_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.witzenberg_lm import WitzenbergLmSource, MOCK_HTML
    src = WitzenbergLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_witzenberg_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.witzenberg_lm import WitzenbergLmSource
    src = WitzenbergLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
