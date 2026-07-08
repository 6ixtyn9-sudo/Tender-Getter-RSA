"""Tests for the Khai-Ma LM tender source plug-in."""
import pytest


def test_khara_hais_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.khara_hais_lm_tenders import KharaHaisLmSource
    src = KharaHaisLmSource()
    assert src.source_id == "khara_hais_lm_tenders"
    assert src.live is False


def test_khara_hais_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.khara_hais_lm_tenders import KharaHaisLmSource, MOCK_HTML
    src = KharaHaisLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_khara_hais_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.khara_hais_lm_tenders import KharaHaisLmSource
    src = KharaHaisLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
