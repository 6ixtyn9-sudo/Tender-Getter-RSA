"""Tests for the Makhuduthamaga LM tender source plug-in."""
import pytest


def test_makhuduthamaga_lm_source_initialization():
    from tender_getter.sources.local_municipalities.makhuduthamaga_lm import MakhuduthamagaLmSource
    src = MakhuduthamagaLmSource()
    assert src.source_id == "makhuduthamaga_lm"
    assert isinstance(src.live, bool)


def test_makhuduthamaga_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.makhuduthamaga_lm import MakhuduthamagaLmSource, MOCK_HTML
    src = MakhuduthamagaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_makhuduthamaga_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.makhuduthamaga_lm import MakhuduthamagaLmSource
    src = MakhuduthamagaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
