"""Tests for the Khai-Ma LM tender source plug-in."""
import pytest


def test_khara_hais_lm_source_initialization():
    from tender_getter.sources.local_municipalities.khara_hais_lm import KharaHaisLmSource
    src = KharaHaisLmSource()
    assert src.source_id == "khara_hais_lm"
    assert isinstance(src.live, bool)


def test_khara_hais_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.khara_hais_lm import KharaHaisLmSource, MOCK_HTML
    src = KharaHaisLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_khara_hais_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.khara_hais_lm import KharaHaisLmSource
    src = KharaHaisLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
