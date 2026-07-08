"""Tests for the Thulamela Local Municipality tender source plug-in."""
import pytest


def test_thulamela_lm_source_initialization():
    from tender_getter.sources.local_municipalities.thulamela_lm import ThulamelaLmSource
    src = ThulamelaLmSource()
    assert src.source_id == "thulamela_lm"
    assert src.live is True


def test_thulamela_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.thulamela_lm import ThulamelaLmSource, MOCK_HTML
    src = ThulamelaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_thulamela_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.thulamela_lm import ThulamelaLmSource
    src = ThulamelaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
