"""Tests for the Chris Hani LM tender source plug-in."""
import pytest


def test_chris_hani_lm_source_initialization():
    from tender_getter.sources.local_municipalities.chris_hani_lm import ChrisHaniLmSource
    src = ChrisHaniLmSource()
    assert src.source_id == "chris_hani_lm"
    assert src.live is False


def test_chris_hani_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.chris_hani_lm import ChrisHaniLmSource, MOCK_HTML
    src = ChrisHaniLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_chris_hani_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.chris_hani_lm import ChrisHaniLmSource
    src = ChrisHaniLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
