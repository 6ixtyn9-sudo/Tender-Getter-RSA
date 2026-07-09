"""Tests for the Nkosi LM tender source plug-in."""
import pytest


def test_nkosi_lm_source_initialization():
    from tender_getter.sources.local_municipalities.nkosi_lm import NkosiLmSource
    src = NkosiLmSource()
    assert src.source_id == "nkosi_lm"
    assert src.live is False


def test_nkosi_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.nkosi_lm import NkosiLmSource, MOCK_HTML
    src = NkosiLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nkosi_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.nkosi_lm import NkosiLmSource
    src = NkosiLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
