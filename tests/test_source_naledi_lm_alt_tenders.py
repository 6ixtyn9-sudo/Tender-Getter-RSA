"""Tests for the Naledi (alt) tender source plug-in."""
import pytest


def test_naledi_lm_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.naledi_lm_alt_tenders import NalediLmAltSource
    src = NalediLmAltSource()
    assert src.source_id == "naledi_lm_alt_tenders"
    assert src.live is False


def test_naledi_lm_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.naledi_lm_alt_tenders import NalediLmAltSource, MOCK_HTML
    src = NalediLmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_naledi_lm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.naledi_lm_alt_tenders import NalediLmAltSource
    src = NalediLmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
