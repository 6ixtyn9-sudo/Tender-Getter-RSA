"""Tests for the Ngqushwa LM (alt) tender source plug-in."""
import pytest


def test_ngqushwa_lm_alt_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.ngqushwa_lm_alt_tenders import NgqushwaLmAltSource
    src = NgqushwaLmAltSource()
    assert src.source_id == "ngqushwa_lm_alt_tenders"
    assert src.live is False


def test_ngqushwa_lm_alt_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.ngqushwa_lm_alt_tenders import NgqushwaLmAltSource, MOCK_HTML
    src = NgqushwaLmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ngqushwa_lm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ngqushwa_lm_alt_tenders import NgqushwaLmAltSource
    src = NgqushwaLmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
