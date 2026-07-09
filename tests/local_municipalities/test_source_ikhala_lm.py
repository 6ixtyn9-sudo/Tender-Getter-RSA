"""Tests for the Ikhala LM tender source plug-in."""
import pytest


def test_ikhala_lm_source_initialization():
    from tender_getter.sources.local_municipalities.ikhala_lm import IkhalaLmSource
    src = IkhalaLmSource()
    assert src.source_id == "ikhala_lm"
    assert src.live is False


def test_ikhala_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.ikhala_lm import IkhalaLmSource, MOCK_HTML
    src = IkhalaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ikhala_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ikhala_lm import IkhalaLmSource
    src = IkhalaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
