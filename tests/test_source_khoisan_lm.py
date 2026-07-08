"""Tests for the Khoisan LM tender source plug-in."""
import pytest


def test_khoisan_lm_source_initialization():
    from tender_getter.sources.local_municipalities.khoisan_lm import KhoisanLmSource
    src = KhoisanLmSource()
    assert src.source_id == "khoisan_lm"
    assert src.live is False


def test_khoisan_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.khoisan_lm import KhoisanLmSource, MOCK_HTML
    src = KhoisanLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_khoisan_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.khoisan_lm import KhoisanLmSource
    src = KhoisanLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
