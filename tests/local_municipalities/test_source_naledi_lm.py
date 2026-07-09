"""Tests for the Naledi LM tender source plug-in."""
import pytest


def test_naledi_lm_source_initialization():
    from tender_getter.sources.local_municipalities.naledi_lm import NalediLmSource
    src = NalediLmSource()
    assert src.source_id == "naledi_lm"
    assert isinstance(src.live, bool)


def test_naledi_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.naledi_lm import NalediLmSource, MOCK_HTML
    src = NalediLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_naledi_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.naledi_lm import NalediLmSource
    src = NalediLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
