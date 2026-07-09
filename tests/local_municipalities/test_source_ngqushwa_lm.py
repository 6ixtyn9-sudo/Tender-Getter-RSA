"""Tests for the Ngqushwa Local Municipality tender source plug-in."""
import pytest


def test_ngqushwa_lm_source_initialization():
    from tender_getter.sources.local_municipalities.ngqushwa_lm import NgqushwaLmSource
    src = NgqushwaLmSource()
    assert src.source_id == "ngqushwa_lm"
    assert isinstance(src.live, bool)


def test_ngqushwa_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.ngqushwa_lm import NgqushwaLmSource, MOCK_HTML
    src = NgqushwaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ngqushwa_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ngqushwa_lm import NgqushwaLmSource
    src = NgqushwaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
