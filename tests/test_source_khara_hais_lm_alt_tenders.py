"""Tests for the Khai-Ma (alt) tender source plug-in."""
import pytest


def test_khara_hais_lm_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.khara_hais_lm_alt_tenders import KharaHaisLmAltSource
    src = KharaHaisLmAltSource()
    assert src.source_id == "khara_hais_lm_alt_tenders"
    assert src.live is False


def test_khara_hais_lm_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.khara_hais_lm_alt_tenders import KharaHaisLmAltSource, MOCK_HTML
    src = KharaHaisLmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_khara_hais_lm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.khara_hais_lm_alt_tenders import KharaHaisLmAltSource
    src = KharaHaisLmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
