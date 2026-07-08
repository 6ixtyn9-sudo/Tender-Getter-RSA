"""Tests for the Witzenberg LM tender source plug-in."""
import pytest


def test_witzenberg_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.witzenberg_lm_tenders import WitzenbergLmSource
    src = WitzenbergLmSource()
    assert src.source_id == "witzenberg_lm_tenders"
    assert src.live is False


def test_witzenberg_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.witzenberg_lm_tenders import WitzenbergLmSource, MOCK_HTML
    src = WitzenbergLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_witzenberg_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.witzenberg_lm_tenders import WitzenbergLmSource
    src = WitzenbergLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
