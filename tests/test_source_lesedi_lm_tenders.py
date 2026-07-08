"""Tests for the Lesedi Local Municipality tender source plug-in."""
import pytest


def test_lesedi_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.lesedi_lm_tenders import LesediLmSource
    src = LesediLmSource()
    assert src.source_id == "lesedi_lm_tenders"
    assert src.live is True


def test_lesedi_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.lesedi_lm_tenders import LesediLmSource, MOCK_HTML
    src = LesediLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lesedi_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.lesedi_lm_tenders import LesediLmSource
    src = LesediLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
