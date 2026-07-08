"""Tests for the Ngqushwa Local Municipality tender source plug-in."""
import pytest


def test_ngqushwa_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.ngqushwa_lm_tenders import NgqushwaLmSource
    src = NgqushwaLmSource()
    assert src.source_id == "ngqushwa_lm_tenders"
    assert src.live is True


def test_ngqushwa_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.ngqushwa_lm_tenders import NgqushwaLmSource, MOCK_HTML
    src = NgqushwaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ngqushwa_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ngqushwa_lm_tenders import NgqushwaLmSource
    src = NgqushwaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
