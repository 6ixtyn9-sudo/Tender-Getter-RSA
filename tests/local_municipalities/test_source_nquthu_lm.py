"""Tests for the Nquthu LM tender source plug-in."""
import pytest


def test_nquthu_lm_source_initialization():
    from tender_getter.sources.local_municipalities.nquthu_lm import NquthuLmSource
    src = NquthuLmSource()
    assert src.source_id == "nquthu_lm"
    assert isinstance(src.live, bool)


def test_nquthu_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.nquthu_lm import NquthuLmSource, MOCK_HTML
    src = NquthuLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nquthu_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.nquthu_lm import NquthuLmSource
    src = NquthuLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
